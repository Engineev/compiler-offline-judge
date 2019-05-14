import subprocess
from . import assembly
from . import testcase


def check_result(case, res):
    time = res.time
    # type: (testcase, subprocess.CompletedProcess) -> (bool, str)
    if case.assertion == "output":
        output = '\n'.join([x.strip()
                            for x in res.stdout.decode('utf-8').split('\n')])
        if output.strip() == case.output.strip():
            if res.returncode != 0:
                return True, "(Can not judge)return " + str(res.returncode), time
            return True, " ", time
        
        with open("my.debug", "w") as f:
            f.write(output)
        with open("std.debug", "w") as f:
            f.write(case.output)

        return False, "output dismatched", time
    
    if case.assertion == "exitcode":
        if res.returncode == case.exitcode:
            return True, " ", time
        return False, "exitcode dismatched", time
    if case.assertion == "runtimeerror":
        if res.returncode != 0:
            return True, " ", time
        return False, "Runtime error expected", time

    return False, "Unknown Error", time
    pass


def test_with_ir_interpreter(case, ir_src, ir_interpreter_path):
    # type: (testcase, str, str) -> (bool, str)
    with open("./__ir.ll", "w") as f:
        f.write(ir_src)
    try:
        res = subprocess.run([ir_interpreter_path, "./__ir.ll"],
                             input=case.input.encode('utf-8'),
                             stdout=subprocess.PIPE,
                             timeout=case.timeout * 100)
    except subprocess.TimeoutExpired:
        return False, "TLE" # NOTE: Tag: changed here with True(Origin False)
    return check_result(case, res)


def test_with_asm(case, asm_src):
    # type: (testcase, str) -> (bool, str)
    with open("./__a.asm", "w") as f:
        f.write(asm_src)
    try:
        flag, res = assembly.run("__a.asm", input=case.input.encode('utf-8'),
                                 timeout=case.timeout)
    except subprocess.TimeoutExpired:
        return False, "TLE", " " # NOTE: Tag: changed here with True(Origin False)
    if not flag:
        return False, res
    return check_result(case, res)


def test(case, bash_path, ir_interpreter_path=""):
    # type: (testcase, str, str) -> (bool, str)
    
    res = subprocess.run(["bash", bash_path], input=case.src.encode('utf-8'),
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    if ir_interpreter_path:
        return test_with_ir_interpreter(case, res.stdout.decode('utf-8'),
                                        ir_interpreter_path)
    return test_with_asm(case, res.stdout.decode('utf-8'))

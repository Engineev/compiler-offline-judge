import subprocess
from . import assembly
from . import testcase


def check_result(case, res):
    # type: (testcase, subprocess.CompletedProcess) -> (bool, str)
    if case.assertion == "output":
        if res.returncode != 0:
            return False, "Unexpected runtime error"
        output = '\n'.join([x.strip()
                            for x in res.stdout.decode('utf-8').split('\n')])
        if output.strip() == case.output.strip():
            return True, ""
        return False, "output dismatched"
    if case.assertion == "exitcode":
        if res.returncode == case.exitcode:
            return True, ""
        return False, "exitcode dismatched"
    if case.assertion == "runtimeerror":
        if res.returncode != 0:
            return True, ""
        return False, "Runtime error expected"
    return False, "Unknown"
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
        return False, "TLE"
    return check_result(case, res)


def test_with_asm(case, asm_src):
    # type: (testcase, str) -> (bool, str)
    with open("./__a.asm", "w") as f:
        f.write(asm_src)
    try:
        flag, res = assembly.run("__a.asm", input=case.input.encode('utf-8'),
                                 timeout=case.timeout)
    except subprocess.TimeoutExpired:
        return False, "TLE"
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

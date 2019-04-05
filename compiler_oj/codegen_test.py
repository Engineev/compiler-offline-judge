import subprocess
import os
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
    # build
    res = subprocess.run("nasm -felf64 -o __a.o __a.asm", shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        return False, "The nasm code can not be compiled.\n" + \
               res.stderr.decode('utf8')
    # link
    res = subprocess.run("gcc -o __a.out -O0 --static -fno-pie -no-pie __a.o",
                         shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    if res.returncode != 0:
        return False, "The nasm code can not be linked.\n" + \
               res.stderr.decode('utf8')
    # run
    try:
        res = subprocess.run("./__a.out", shell=True,
                             input=case.input.encode('utf8'),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL,
                             timeout=case.timeout)
    except UnicodeDecodeError:
        return False, "The output can not be decoded"
    return check_result(case, res.stdout.decode('utf8'))


def test(case, config):
    assert type(case) == testcase.TestCase
    bash_path = os.path.join(config['bash_dir'], '__codegen.bash')
    res = subprocess.run(['bash', bash_path], input=case.src.encode('utf8'),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result_src = res.stdout.decode('utf8')
    if config['ir_interpreter']:
        return test_with_ir_interpreter(case, result_src,
                                        config['ir_interpreter'])
    return test_with_asm(case, result_src)



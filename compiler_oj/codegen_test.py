from . import assembly
from . import testcase

def test(testcase, bash_path):
    res = assembly.run(bash_path, input=testcase.src)
    with open("__a.asm") as f:
        f.write(res)
        res = assembly.run("./__a.asm", input=testcase.input)
        if testcase.assertion == "output":
            return res.stdout == testcase.output
        if testcase.assertion == "exitcode":
            return res.returncode == testcase.exitcode
        if testcase.assertion == "runtimeerror":
            return res.returncode != 0
    return False
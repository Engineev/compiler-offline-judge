import subprocess
from . import assembly
from . import testcase

def test(testcase, bash_path):
    res = subprocess.run(["bash", bash_path], universal_newline=True,
        input=testcase.src, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    with open("./__a.asm", "w") as f:
        f.write(res.stdout)
    
    try:
        res = assembly.run("__a.asm", input=testcase.input, timeout=testcase.timeout)
    except subprocess.TimeoutExpired:
        return (False, "TLE")

    if testcase.assertion == "output":
        if res.returncode != 0:
            return (False, "Unexpected runtime error")
        output = '\n'.join(list(map(lambda x: x.strip(), res.stdout.split('\n'))))
        if output.strip() == testcase.output.strip():
            return (True, "")
        # print("\n")
        # print(res.stdout)
        # print(output)
        # print(testcase.output)
        return (False, "output dismatched")
    if testcase.assertion == "exitcode":
        if res.returncode == testcase.exitcode:
            return (True, "")
        return (False, "exitcode dismatched")
    if testcase.assertion == "runtimeerror":
        if res.returncode != 0:
            return (True, "")
        return (False, "Runtime error expected")
    return (False, "Unknown")
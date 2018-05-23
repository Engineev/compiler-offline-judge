import subprocess
from . import testcase

def test(testcase, bash_path):
    res = subprocess.run(["bash", bash_path], 
        input=testcase.src, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        encoding='ascii')
    if testcase.assertion == "success_compile" and res.returncode != 0:
        return (False, "Build failed unexpectedly")
    if testcase.assertion == "failure_compile" and res.returncode == 0:
        return (False, "The build should fail")
    return (True, "")
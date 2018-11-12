import subprocess
from . import testcase


def test(case: testcase.TestCase, bash_path):
    res = subprocess.run(["bash", bash_path], input=case.src.encode('utf-8'),
                         stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if case.assertion == "success_compile" and res.returncode != 0:
        message = "Build failed unexpectedly.\n"
        message += res.stderr.decode('utf-8')
        return False, message
    if case.assertion == "failure_compile" and res.returncode == 0:
        return False, "The build should fail"
    return True, ""

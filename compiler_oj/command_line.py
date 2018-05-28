import argparse
import json
import os
import sys
import subprocess

from . import testcase
from . import codegen_test
from . import semantic_test


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config",
                        help="the path to the config file (default=\"./config.json\")",
                        type=str, default="./config.json")
    parser.add_argument("-t", "--testcases_dir",
                        help="the path to testcases(default in config file)", type=str, default="")
    parser.add_argument("-b", "--bash_dir",
                        help="the path to bash file(default in config file)", type=str, default="")
    parser.add_argument("-p", "--phases",
                        help="the test phase(default in config file)", type=str, default="")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)
    if args.testcases_dir != "":
        config["testcases_dir"] = args.testcases_dir
    if args.bash_dir != "":
        config["bash_dir"] = args.bash_dir
    if args.phases != "":
        config["phases"] = [phase.strip() for phase in args.phases.split(",")]

    print("building...", end=" ")
    sys.stdout.flush()
    res = subprocess.run(["bash", os.path.join(config["bash_dir"], "build.bash")],
                         stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if res.returncode != 0:
        print("Failed.")
        print(str(res.stderr))
        return
    print("Passed.")

    cases = list(filter(lambda x: x.phase in config["phases"],
                        testcase.read_testcases(config["testcases_dir"])))
    cases_failed = []
    print(str(len(cases)) + " testcases")
    passNum = 0
    testNum = 0
    for test in cases:
        print("running " + test.filename + "...", end=" ")
        sys.stdout.flush()
        phase = test.phase.partition(" ")[0]
        if phase == "codegen":
            res = codegen_test.test(
                test, os.path.join(config["bash_dir"], "codegen.bash"))
        elif phase == "semantic":
            res = semantic_test.test(
                test, os.path.join(config["bash_dir"], "semantic.bash"))
        else:
            print(phase + " is unsupported currently")
            continue
        testNum += 1
        if res[0]:
            passNum += 1
            print("\033[32mPassed.\033[0m")
        else:
            cases_failed.append(test.filename)
            print("\033[31mFailed: " + res[1] + "\033[0m")

    if len(cases_failed) == 0:
        print("All testcases have been passed")
        return
    print("testcases failed:")
    for name in cases_failed:
        print(name)
    print("Pass rate: {}/{}".format(passNum, testNum))
    subprocess.run("rm *.asm *.out *.o", shell=True)

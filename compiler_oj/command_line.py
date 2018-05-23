import argparse
import json
import os
import sys
import subprocess

from . import testcase
from . import codegen_test

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", 
        help="the path to the config file", type=str)
    args = parser.parse_args()
    
    with open(args.config) as f:
        config = json.load(f)

    print("building...", end=' ')
    sys.stdout.flush()
    res = subprocess.run(["bash", os.path.join(config["bash_dir"], "build.bash")],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        print("Failed.")
        return
    print("Passed.")

    cases = filter(lambda x: x.phase in config["phases"], 
        testcase.read_testcases(config["testcases_dir"]))
    cases_failed = []
    for test in cases:
        if test.phase.partition(' ')[0] == "codegen":
            print("running " + test.filename + "...", end=' ')
            sys.stdout.flush()
            res = codegen_test.test(
                    test, os.path.join(config["bash_dir"], "codegen.bash"))
            if res[0]:
                print("Passed.")
            else:
                cases_failed.append(test.filename)
                print("Failed: " + res[1])
                # return
    print("testcases failed:")
    for name in cases_failed:
        print(name)
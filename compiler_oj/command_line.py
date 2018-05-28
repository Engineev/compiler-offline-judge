import argparse
import json
import os
import sys
import subprocess

from . import testcase
from . import codegen_test
from . import semantic_test

def replaceNewlines(dst, src):
    with open(dst, "w") as dst_f:
        with open(src) as src_f:
            content = src_f.read()
        dst_f.write(content.replace("\r\n", "\n"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", 
        help="the path to the config file (default=\"./config.json\")", 
        type=str, default="./config.json")
    args = parser.parse_args()
    
    with open(args.config) as f:
        config = json.load(f)

    for name in ["build.bash", "semantic.bash", "codegen.bash", "optim.bash"]:
        src = os.path.join(config["bash_dir"], name)
        if not os.path.isfile(src):
            continue
        dst = os.path.join(config["bash_dir"], "__" + name)
        replaceNewlines(dst, src)

    print("building...", end=' ')
    sys.stdout.flush()
    res = subprocess.run(
        ["bash", os.path.join(config["bash_dir"], "__build.bash")],
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
    for test in cases:
        print("running " + test.filename + "...", end=' ')
        sys.stdout.flush()
        phase = test.phase.partition(' ')[0]
        if  phase == "codegen":    
            res = codegen_test.test(
                test, os.path.join(config["bash_dir"], "__codegen.bash"))
        elif phase == "semantic":
            res = semantic_test.test(
                test, os.path.join(config["bash_dir"], "__semantic.bash"))
        else:
            print(phase + " is unsupported currently")
            continue
        if res[0]:
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
    subprocess.run("rm __a.asm __a.o __a.out __build.bash __semantic.bash __codegen.bash", 
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
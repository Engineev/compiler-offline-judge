import argparse
import json
import os
import sys
import subprocess
import pickle

from . import testcase
from . import codegen_test
from . import semantic_test


def replace_newlines(dst, src):
    with open(dst, "w") as dst_f:
        with open(src) as src_f:
            content = src_f.read()
        dst_f.write(content.replace("\r\n", "\n"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config",
                        help="the path to the config file " +
                             "(default=\"./config.json\")",
                        type=str, default="./config.json")
    parser.add_argument("-t", "--testcases_dir",
                        help="the path to testcases(default in config file)",
                        type=str, default="")
    parser.add_argument("-b", "--bash_dir",
                        help="the path to bash file(default in config file)",
                        type=str, default="")
    parser.add_argument("-p", "--phases",
                        help="the test phase(default in config file)",
                        type=str, default="")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)
    if args.testcases_dir != "":
        config["testcases_dir"] = args.testcases_dir
    if args.bash_dir != "":
        config["bash_dir"] = args.bash_dir
    if args.phases != "":
        config["phases"] = [phase.strip() for phase in args.phases.split(",")]

    for name in ["build.bash", "semantic.bash", "codegen.bash", "optim.bash"]:
        src = os.path.join(config["bash_dir"], name)
        if not os.path.isfile(src):
            continue
        dst = os.path.join(config["bash_dir"], "__" + name)
        replace_newlines(dst, src)

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

    cases = [t for t in testcase.read_testcases(config['testcases_dir'])
             if t.phase in config['phases']]
    cases.sort(key=lambda x: x.filename)
    cases_failed = []
    print(str(len(cases)) + " testcases")
    pass_num = 0
    test_num = 0
    for test in cases:
        print("running " + test.filename + "...", end=" ")
        sys.stdout.flush()
        phase = test.phase.partition(" ")[0]
        if phase == "codegen":
            res = codegen_test.test(
                test, os.path.join(config["bash_dir"], "__codegen.bash"),
                config["ir_interpreter"])
        elif phase == "semantic":
            res = semantic_test.test(
                test, os.path.join(config["bash_dir"], "__semantic.bash"))
        elif phase == "optim":
            res = codegen_test.test(
                test, os.path.join(config["bash_dir"], "__optim.bash"))
        else:
            print(phase + " is unsupported currently")
            continue
        test_num += 1
        if res[0]:
            pass_num += 1
            print("\033[32mPassed. " + res[1] + "\033[0m")
        else:
            cases_failed.append(test.filename)
            print("\033[31mFailed: " + res[1] + "\033[0m")

    if len(cases_failed) == 0:
        print("All testcases have been passed")
    else:
        print("testcases failed:")
        for name in cases_failed:
            print(name)
        print("Pass rate: {}/{}".format(pass_num, test_num))

    subprocess.run("rm __a.asm __a.o __a.out",
                   shell=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    rm = "rm " + config['bash_dir'] + "/__*.bash"
    subprocess.run(rm, shell=True)
    subprocess.run("rm ./__ir.ll", shell=True)

    # TODO
    # print("\nComparing with the last run: ")
    # log_filename = "oj-result.data"
    # last_failed = []
    # try:
    #     with open(log_filename, "rb") as f:
    #         last_failed = pickle.load(f)
    # except:
    #     print("The data of the last run can not be read")
    # with open(log_filename, "wb") as f:
    #     pickle.dump(cases_failed, f)
    #
    # print("\033[32m", end='')
    # for name in set(last_failed) - set(cases_failed):
    #     print("+ " + name)
    # print("\033[0m" + "\033[31m")
    # for name in set(cases_failed) - set(last_failed):
    #     print("- " + name)
    # print("\033[0m", end='')


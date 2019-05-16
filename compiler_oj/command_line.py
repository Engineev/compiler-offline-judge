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
    # args
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
    parser.add_argument("-s", "--speedup",
                        help="the time command(default in config file)",
                        type=float)
    parser.add_argument("-r", "--run",
                        help="the run phase(default in config file)",
                        type=str, default="normal")
    parser.add_argument("-d", "--debug",
                        help="debug",
                        action='store_true')
    args = parser.parse_args()

    # config.json
    with open(args.config) as f:
        config = json.load(f)
    if args.testcases_dir != "":
        config["testcases_dir"] = args.testcases_dir
    if args.bash_dir != "":
        config["bash_dir"] = args.bash_dir
    if args.phases != "":
        config["phases"] = [phase.strip() for phase in args.phases.split(",")]
    if args.speedup != None:
        config["speedup"] = args.speedup
    if args.run != "":
        config["run"] = args.run

    if config["run"] == "codegen":
        config["speedup"] = 0.2

    # bash
    for name in ["build.bash", "semantic.bash", "codegen.bash", "optim.bash"]:
        src = os.path.join(config["bash_dir"], name)
        if not os.path.isfile(src):
            print("Not found " + src)
            continue
        dst = os.path.join(config["bash_dir"], "" + name)
        # replace_newlines(dst, src)

    # build
    # print(args)
    if not args.debug:
        print("building...", end=' ')
        sys.stdout.flush()
        res = subprocess.run(
            ["bash", os.path.join(config["bash_dir"], "build.bash")],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        if res.returncode != 0:
            print("Failed.")
            print(str(res.stderr))
            clear_cache()
            print("\033[91m build Failed. \033[0m")
            sys.stdout.flush()
            return

        print("Passed.")
        print("Using "+config["run"]+" method with " +
              str(config["speedup"]) + " speed")
        print("Start Path: "+ os.path.abspath(config["bash_dir"]))

    # read cases
    cases = [t for t in testcase.read_testcases(config['testcases_dir'], config['speedup'])
             if t.phase in config['phases']]
    cases.sort(key=lambda x: x.filename)
    cases_failed = {}
    cases_suc = {}
    pass_num = 0
    test_num = 0

    # run cases
    for test in cases:
        time = [100.0, "null"]
        res = ()
        print("running " + test.filename + "...", end=" ")
        sys.stdout.flush()
        phase = test.phase.partition(" ")[0]
        if phase == "semantic":
            res = semantic_test.test(
                test, os.path.join(config["bash_dir"], "semantic.bash"))
            res = res + ("semantic",)
        elif phase == "codegen":
            res = codegen_test.test(
                test, os.path.join(config["bash_dir"], "codegen.bash"))
            res = res + ("codegen",)
            if res[0] and time[0] > res[2]:
                time[0] = res[2]
                time[1] = "codegen"
            if res[0] and config["run"] == "shuffle":
                res = codegen_test.test(
                    test, os.path.join(config["bash_dir"], "optim.bash"))
                res = res + ("optim",)
                if res[0] and time[0] > res[2]:
                    time[0] = res[2]
                    time[1] = "optim"
        elif phase == "optim":
            if config["run"] == "codegen":
                res = codegen_test.test(
                    test, os.path.join(config["bash_dir"], "codegen.bash"))
                res = res + ("codegen",)
                if res[0] and time[0] > res[2]:
                    time[0] = res[2]
                    time[1] = "codegen"
            else:
                res = codegen_test.test(
                    test, os.path.join(config["bash_dir"], "optim.bash"))
                res = res + ("optim",)
                if res[0] and time[0] > res[2]:
                    time[0] = res[2]
                    time[1] = "optim"
            if res[0] and config["run"] == "shuffle":
                res = codegen_test.test(
                    test, os.path.join(config["bash_dir"], "codegen.bash"))
                res = res + ("codegen",)
                if res[0] and time[0] > res[2]:
                    time[0] = res[2]
                    time[1] = "codegen"
        else:
            print(phase + " is unsupported currently")
            continue

        test_num += 1
        s = str(round(time[0], 4)) + "s with " + time[1]
        # res[0]:true/false; 1:msg; 2:time; 3:append
        leng = len(res)
        for i in range(leng, 4):
            res += ("",)

        if res[0] and config["speedup"] > 1.0:
            pass_num += 1
            print("\033[32mPassed. " + " " + s + "\033[0m")
            cases_suc[test.filename] = [time[0], time[1]]
        elif ~res[0] and config["speedup"] > 1.0:
            print("\033[31mFailed at " + res[3] +
                  ": " + res[1] + " " + s + "\033[0m")
            cases_failed[test.filename] = [res[1], res[3]]
        elif res[0]:
            pass_num += 1
            cases_suc[test.filename] = [time[0], time[1]]
            print("\033[32mPassed. " + res[1] + "\033[0m")
        else:
            print("\033[31mFailed at " + res[3] + ": " + res[1] + "\033[0m")
            cases_failed[test.filename] = [res[1], res[3]]

    # conclusion
    if pass_num == test_num:
        print("All testcases have been passed")
    else:
        print("testcases failed:")
        # TODO: more info to print
        for case, _ in cases_failed.items():
            print(case)
        print("Pass rate: {}/{}".format(pass_num, test_num))

    clear_cache()
    CompareScore(args, cases_failed, cases_suc)
    return


def CompareScore(args, cases_failed, cases_suc):
    # compare score
    print("\nComparing with the last run: ")
    # [test.filename, res[1](reason), res[3](optim/codegen)
    log_filename = "oj-result-fail-me.data"
    log_filename_s = "oj-result-fail.data"
    last_failed = {}
    cmp = True
    try:
        with open(log_filename, "rb") as f:
            last_failed = pickle.load(f)
    except:
        print("The data of the last run can not be read")
        cmp = False

    if not args.debug:
        with open(log_filename, "wb") as f:
            pickle.dump(cases_failed, f)

    # TODO: more info can be sent out
    if cmp:
        # print(last_failed)
        # print(cases_failed)
        print("\033[32m", end='')
        for name in set(last_failed.keys()) - set(cases_failed.keys()):
            print("+ " + name)
        print("\033[0m" + "\033[31m")
        for name in set(last_failed.keys()) - set(last_failed.keys()):
            print("- " + name)
        print("\033[0m", end='')

    # [test.filename, time[0](time), time[1](optim/codegen)
    log_filename = "oj-result-succ-me.data"
    log_filename_s = "oj-result-succ.data"
    last_succ = {}
    last_succ_s = {}

    cmp = True
    try:
        with open(log_filename, "rb") as f:
            last_succ = pickle.load(f)
        with open(log_filename_s, "rb") as f:
            last_succ_s = pickle.load(f)
    except:
        print("The data of the last run can not be read")
        cmp = False

    if not args.debug:
        with open(log_filename, "wb") as f:
            pickle.dump(cases_suc, f)

    if cmp:
        for name in set(last_succ.keys()) & set(cases_suc.keys()):
            gap = last_succ[name][0] - cases_suc[name][0]
            case = cases_suc[name] if gap > 0 else last_succ[name]
            print(name, ":" + "\033[32mbetter\033[0m" if gap > 0.0 else "\033[31mworse\033[0m" +
                  " ", str(round(gap, 4)), " with " + case[1])
        print("\n\n")
        for name in set(last_succ_s.keys()) & set(cases_suc.keys()):
            gap = last_succ_s[name][0] - cases_suc[name][0]
            case = cases_suc[name] if gap > 0 else last_succ_s[name]
            print(name, ":" + "\033[32mbetter\033[0m" if gap > 0.0 else "\033[31mworse\033[0m" +
                  " ", str(round(gap, 4)), " with " + case[1])
    return


def clear_cache():
    # clear cache
    subprocess.run("rm -f __a.asm __a.o __a.out",
                   shell=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    # rm = "rm -f " + config['bash_dir'] + "/__*.bash"
    # subprocess.run(rm, shell=True)
    subprocess.run("rm -f ./__ir.ll", shell=True)
    # subprocess.run("rm -f ./*.debug", shell=True)
    return

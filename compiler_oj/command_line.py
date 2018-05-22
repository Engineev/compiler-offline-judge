import argparse
import json
import os

from . import testcase
from . import codegen_test

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", 
        help="the path to the config file", type=str)
    args = parser.parse_args()
    
    with open(args.config) as f:
        config = json.load(f)
        cases = filter(lambda x: x.phase in config["phases"], 
            testcase.read_testcases(config["testcases_dir"]))
        for test in cases:
            if test.phase.partition(' ')[0] == "codegen":
                print("running " + test.filename + "...", end=' ')
                res = codegen_test.test(
                        config["testcases_dir"], 
                        os.path.join(config["bash_dir"], "codegen.bash"))
                if res:
                    print("Passed")
                else:
                    print("Failed")
                
    
    
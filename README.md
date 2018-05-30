# compiler-offline-judge

The offline version of acm-compiler-judge. The process is still ongoing.
Only the semantic check and the codegen part have been completed and they
have not been tested yet.

## Getting Started

### Install

To install compiler-oj, just `cd` into the repository directory and

`pip3 install .`

Maybe you need to run

`export PATH="$HOME/.local/bin:$PATH"`

in order to run the judge by `compiler-oj` in the terminal.

### Write the config file

A json file is required to tell the judge what to do. A sample config
file is given in `doc/`.

### Test

`compiler-oj -c='PATH/TO/THE/CONFIG/FILE'`

The default value of `-c` is `./config.json`

## Get all testcases from website

* This part was written by TimerChen
* The `download.sh` only test on Ubuntu with python3.6, which could not work on other environments.

### Download all cases
In ./TestCases directory, use `python3 download.py` to get all testcases.

### Download cases you need
Modify the `./TestCases/download.py` file, and change the varaiable `last_test_log` to the website of your last submission.

Like: `last_test_log = 'http://blacko.cn:6002/Compiler/build/2161'`

Then it will only download what you need to test.

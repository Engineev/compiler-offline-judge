# compiler-offline-judge

The offline version of acm-compiler-judge.

## Requirement

* python3 (version >= 3.5)

## Getting Started

### Install (Optional)

To install compiler-oj, just `cd` into the repository directory and

`pip3 install .`

Maybe you need to run

`export PATH="$HOME/.local/bin:$PATH"`

in order to run the judge by `compiler-oj` in the terminal.


### Write the config file

A json file is required to tell the judge what to do. A sample config
file is given in `doc/`.

### Test

`cd` into the repository directory and `python3 ./run.py`.  If compiler-oj has
been installed, you can also use

`compiler-oj -c='PATH/TO/THE/CONFIG/FILE'`

to start a test. The default value of `-c` is `./config.json`



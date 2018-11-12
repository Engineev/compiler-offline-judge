# compiler-offline-judge

The offline version of acm-compiler-judge.

## Getting Started

### Run without install

TODO

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



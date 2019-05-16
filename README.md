# compiler-offline-judge

The offline version of acm-compiler-judge.


## Change Note

### Warn: Do not delete key of config.json

### add order in config.json

### robuster
> `shuffle`: means run without check timeout with selected data sets with codegen and optim.bash
eg: sel `optim extend` and `shuffle` will run both codegen and optim on `optim extend` set.
> `normal`(default): means run specific tests with specific data sets
eg: sel `optim extend` `codegen extend` and `normal` will run codegen on `codegen extend` and optim on `optim extend` set.

> `codegen`: checkout codegen rightness(timeout*5) with all files

### speedup for powerful compiler
> set speed for your test to get high scores

> add function to output run-time

### Add cmp function to Compare with last run

### Add Dump output in `codegen` when output not matched

### if debug -> no flush of last data

### remove `__*.bash` like temp files

> to avoid produce files if build failed

> add color with build failed

> add clear cache function with build failed

### support more src-test folders

### 

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



# compiler-offline-judge

**UNDER DEVELOPMENT**

The offline version of acm-compiler-judge. The process is still ongoing.
Only the semantic check part has been completed and it has not been tested
yet.

## Getting Start

### Install

To install compiler-oj, just `cd` into the repository directory and 

`pip3 install .`

Maybe you need to run 

`export PATH="$HOME/.local/bin:$PATH"`

in order to run the judge by `compiler-oj` in the terminal.

### Write the config file

A json file is required to tell the judge what to do. A sample config
file is given in doc/.

### Test

`compiler-oj -c='PATH/TO/THE/CONFIG/FILE'`

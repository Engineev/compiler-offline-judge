# compiler-offline-judge

The offline version of acm-compiler-judge. The process is still ongoing.
Only the semantic check part has been completed and it has not been tested
yet.

## Requirement

  * CMake
  * Boost
  * NASM (for codegen and optim)

## Tutorial (TODO)

Use `-h` for more information about the program arguments. 
A sample usage is shown bellow.

`./compiler-oj -T test --phase="semantic pretest" --cases-dir="./TestCases/" --bash-dir="./Bash/"`

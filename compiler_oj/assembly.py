import subprocess

def run(path, input=None, timeout=None):
    res = subprocess.run("nasm -felf64 -o __a.o " + path, shell=True, 
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        return (False, "The nasm code can not be compiled.")
    res = subprocess.run("gcc -o __a.out -O0 -static __a.o", shell=True,
       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        return (False, "The nasm code can not be linked")
    return (True, subprocess.run("./__a.out", universal_newlines=True,
        input=input, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        timeout=timeout))
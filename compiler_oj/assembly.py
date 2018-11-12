import subprocess


def run(path, input=None, timeout=None):
    res = subprocess.run("nasm -felf64 -o __a.o " + path, shell=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        return False, "The nasm code can not be compiled."
    res = subprocess.run("gcc -o __a.out -O0 --static -fno-pie -no-pie __a.o",
                         shell=True, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        return False, "The nasm code can not be linked"

    try:
        res = subprocess.run("./__a.out", input=input, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL, timeout=timeout)
    except UnicodeDecodeError:
        return False, "The output can not be decoded"
    return True, res
    # return (True, subprocess.CompletedProcess("__a.out", ))                                 

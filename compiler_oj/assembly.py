import subprocess

def run(path, input=None, timeout=None):
    res = subprocess.run("nasm -felf64 -o __a.o " + path, shell=True)
    assert(res.returncode == 0)
    res = subprocess.run("gcc -o __a.out -O0 -static __a.o", shell=True)
    assert(res.returncode == 0)
    return subprocess.run("./__a.out", 
        input=input, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        timeout=timeout, encoding='ascii')
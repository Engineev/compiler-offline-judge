import os
import platform
import subprocess

def run(path, input=None, timeout=None):
    os.system("nasm -o __a.o -felf64 " + path)
    os.system("ld __a.o -o __a.out")
    return subprocess.run("./__a.out", 
        input=input, stdout=subprocess.PIPE,
        timeout=timeout, encoding="utf-8")
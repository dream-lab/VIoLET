import os
import sys
import subprocess

command = "./dhrystone/gcc_dry2"

f = open("resultzz","w")
f.write("Dhrystone\n")
f.close()

i = 0
while i<10:
    i += 1
    read, write = os.pipe()
    os.write(write, "99999999")
    os.close(write)
    proc = subprocess.Popen(['./dhrystone/gcc_dry2'],stdin=read,stdout=subprocess.PIPE)
    f = open("resultzz","a+")
    f.write("###################################")
    while True:
        line = proc.stdout.readline()
        if line != '':
            f.write(line)
        else:
            break
    f.close()


import os
import sys
import subprocess


f = open("results-coremark","w")
f.write("Coremark\n")
f.close()

i = 0
while i<15:
    i += 1
    proc = subprocess.Popen(['./coremark.exe'],stdout=subprocess.PIPE)
    f = open("results-coremark","a+")
    f.write("###################################")
    while True:
        line = proc.stdout.readline()
        if line != '':
            f.write(line)
        else:
            break
    f.close()

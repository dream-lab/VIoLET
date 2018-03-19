import os
import sys
import subprocess


f = open("results-coremark4","w")
f.write("Coremark4\n")
f.close()

i = 0
while i<2:
    i += 1
    proc = subprocess.Popen(['./coremark_4.exe'],stdout=subprocess.PIPE)
    f = open("results-coremark4","a+")
    f.write("###################################")
    while True:
        line = proc.stdout.readline()
        if line != '':
            f.write(line)
        else:
            break
    f.close()


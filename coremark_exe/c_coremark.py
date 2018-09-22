import os
import sys
import subprocess
import time

f = open("results-coremark","w")
f.write("Coremark\n")
f.close()

i = 0
start_time = time.time()
end_time = start_time + 3600 # For 8000 seconds running coremark

while True:
    start_time = time.time()
    i += 1
    proc = subprocess.Popen(['./coremark.exe'],stdout=subprocess.PIPE)
    f = open("results-coremark","a+")
    f.write("###################################\n")
    f.write("start_time={0}\n".format(time.time()))
    while True:
        line = proc.stdout.readline()
        if line != '':
            f.write(line)
        else:
            break
    f.write("end_time={0}\n".format(time.time()))
    f.close()

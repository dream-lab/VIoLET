import os
import sys
import subprocess
import time

f = open("results-coremark","w")
f.write("Coremark\n")
f.close()

i = 0
start_time = time.time()
end_time = start_time + 360 # For 8000 seconds running coremark

while start_time < end_time:
    start_time = time.time()
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

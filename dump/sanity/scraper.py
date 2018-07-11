import os
import paramiko
import random
import time
import json
import sys
from datetime import datetime
from threading import Thread

startTime = datetime.now()

sanity = {}

latency_delta = open("latency_delta","w")
for i in range(1,len(sys.argv)):
    sanity[i] = json.load(open(sys.argv[i])) #sys.argv[i]

#print sanity
print "latency"
print
sanity_i = {}
for i in sanity:
    sanity_i = sanity[i]
    for j in sanity_i["latency_numbers"]:
        latency = sanity_i["latency_numbers"][j]
        if(latency["observed_latency_ms"]):
            diff = float(latency["observed_latency_ms"]) - (2*float(sanity_i["expected_latency_ms"]))
            per = diff / (2*float(sanity_i["expected_latency_ms"])) * 100
            print per
            latency_delta.write(str(per)+"\n")
latency_delta.close()


bandwidth_delta = open("bandwidth_delta","w")
print
print "bandwidth"
print

sanity_i = {}
for i in sanity:
    sanity_i = sanity[i]
    for j in sanity_i["bandwidth_numbers"]:
        bw = sanity_i["bandwidth_numbers"][j]
        if(bw["observed_bandwidth_mbps"]):
            diff = float(bw["observed_bandwidth_mbps"]) - float(sanity_i["expected_bandwidth_mbps"])
            per = diff/(float(sanity_i["expected_bandwidth_mbps"])) * 100
            print per
            bandwidth_delta.write(str(per)+"\n")
bandwidth_delta.close()

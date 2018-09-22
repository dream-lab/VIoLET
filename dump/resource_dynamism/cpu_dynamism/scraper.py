import os
import paramiko
import random
import time
import json
import sys
from datetime import datetime
from threading import Thread


infra_config = json.load(open("../../../config/infra_config.json","r"))
devices = infra_config["devices"]
print devices
cpu_dynamism_raw = open("cpu_dynamism_raw.txt","r")
cpu_dynamism_raw.readline()
cpu_dynamism = cpu_dynamism_raw.readlines()
print cpu_dynamism

os.system("mkdir device_logs")

for d in devices:
	print d
	f = open("device_logs/{}.csv".format(d),"w")
	for cpu_dyn in cpu_dynamism:
		dev,dtype,start,end,max_cm,min_cm,prev_cm,new_cm,stat,r,p = cpu_dyn.split(',')
		if d == dev:
			print dev,dtype,prev_cm
			f.write(dev+","+dtype+","+new_cm+"\n")

	f.close()



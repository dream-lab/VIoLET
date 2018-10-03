import json
import time
import sys
import os
import docker
import math
import random
import paramiko

device_down_list = []

def device_down(devices,devices_data,devices_down):
    print 
    print "Active Devices - {}".format(len(devices))
    print 
    for d in devices:
        r = random.uniform(0.0, 1.0)
        #print "Device - {0} r - {1} p - {2}".format(d,r,probability)
	d_type = devices_data[d]["d_type"]
	mttf = devices_data[d]["mttf"]
	mttf_prob = devices_data[d]["mttf_prob"]

	start = time.time()
        
	if r <= mttf_prob:
	    print "Device - {0} r - {1} p - {2}".format(d,r,probability)
            vm_name = deployment_output[d]["host_vm_name"]
            host = container_vm[vm_name]["hostname_ip"]
            user = container_vm[vm_name]["user"]
            key = container_vm[vm_name]["key_path"]
            k = paramiko.RSAKey.from_private_key_file(key)
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(hostname = host, username = user, pkey = k)

            command = "sudo docker stop {}".format(d)
	    start = time.time()
            stdin, stdout, stderr = c.exec_command(command,timeout=60)
	    end = time.time()
	    c.close()
	    mttf_dynamism.write("{0},{1},{2},{3},{4},{5},{6}\n".format(d,d_type,start,end,"yes",r,probability))
            devices.remove(d)
	    devices_down.append(d)
	else:
	    end = time.time()
	    mttf_dynamism.write("{0},{1},{2},{3},{4},{5},{6}\n".format(d,d_type,start,end,"no",r,probability))

    for d in devices_down:
	r = random.uniform(0.0, 1.0)
        #print "Device - {0} r - {1} p - {2}".format(d,r,probability)
        d_type = devices_data[d]["d_type"]
        mttr = devices_data[d]["mttr"]
        mttr_prob = devices_data[d]["mttr_prob"]

        start = time.time()
        
        if r <= mttr_prob:
            print "Device - {0} r - {1} p - {2}".format(d,r,probability)
            vm_name = deployment_output[d]["host_vm_name"]
            host = container_vm[vm_name]["hostname_ip"]
            user = container_vm[vm_name]["user"]
            key = container_vm[vm_name]["key_path"]
            k = paramiko.RSAKey.from_private_key_file(key)
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(hostname = host, username = user, pkey = k)

            command = "sudo docker start {}".format(d)
            start = time.time()
            stdin, stdout, stderr = c.exec_command(command,timeout=60)
            end = time.time()
            c.close()
            mttr_dynamism.write("{0},{1},{2},{3},{4},{5},{6}\n".format(d,d_type,start,end,"yes",r,probability))
            devices.append(d)
	    devices_down.remove(d)
        else:
            end = time.time()
            mttr_dynamism.write("{0},{1},{2},{3},{4},{5},{6}\n".format(d,d_type,start,end,"no",r,probability))
	



infra_config = json.load(open("../../config/infra_config.json"))
vm_config = json.load(open("../../config/vm_config.json"))
device_types = json.load(open("../../config/device_types.json"))
vm_types = json.load(open("../../config/vm_types.json"))
deployment_json = json.load(open("../../config/deployment.json"))
deployment_output = json.load(open("../../dump/infra/deployment_output.json"))
all_devices_list = infra_config["devices"].keys()
container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()

devices = infra_config["devices"]
devices_down = []

control_interval = float(deployment_json["control_interval_secs"])
dynamism_duration = float(deployment_json["dynamism_duration_secs"])

devices_data = {}

for d in devices:
    d_type = devices[d]["device_type"]
    mttf = int(device_types[d_type]["reliability"]["mttf_sec"])
    mttr = int(device_types[d_type]["reliability"]["mttr_sec"])
    mttf_prob = control_interval/mttf
    mttr_prob = control_interval/mttr
    devices_data[d] = {
	"d_type":d_type,
	"mttf":mttf,
	"mttr":mttr,
	"mttf_prob":mttf_prob,
	"mttr_prob":mttr_prob
    }

mttf_dynamism = open("../../dump/resource_dynamism/mttf/mttf_dynamism_raw.txt","w")
mttr_dynamism = open("../../dump/resource_dynamism/mttr/mttr_dynamism_raw.txt","w")



start_time_epoch = time.time()
actual_start_time_epoch = start_time_epoch
start_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(start_time_epoch))
print "\nDevice - {0} start time =  [{1}] \n MTTF = {2} seconds \n".format(dev_type, start_time, mttf)
print "List of {0} devices".format(dev_type)
print devices
print
n = len(devices)

end_time = start_time_epoch + dynamism_duration
print "End time - {0}".format(end_time)

while(True):
    current_time_epoch = time.time()
    if (current_time_epoch > end_time):
	break
    diff = int (current_time_epoch - start_time_epoch)
    if(diff >= control_interval):
	print "\n\n***control_interval***"
    	current_time_epoch = time.time()
    	current_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(current_time_epoch))
    	print "start_time = {0} \tcurrent_time = {1} \ttime elapsed = {2} \tmttf = {3}".format(start_time,current_time,int(current_time_epoch - actual_start_time_epoch), mttf)
        start_time_epoch = time.time()
        val = device_down(devices,devices_data,devices_down)
        if (val == -1):
            break

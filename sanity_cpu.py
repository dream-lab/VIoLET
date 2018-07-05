import os
import paramiko
import random
import time
import json
import threading
import sys
from datetime import datetime
from threading import Thread
from numpy import median

startTime = datetime.now()

infra_config = json.load(open("config/infra_config.json"))
vm_config = json.load(open("config/vm_config.json"))
vm_types = json.load(open("config/vm_types.json"))
sensors =  json.load(open("config/sensor_types.json"))
deployment =  json.load(open("config/deployment.json"))
device_types =  json.load(open("config/device_types.json"))
deployment_output = json.load(open("dump/infra/deployment_output.json"))
eth_ip_dict = json.load(open("dump/infra/eth_ip.json"))

private_networks_dict = infra_config["private_networks"]
public_networks_dict = infra_config["public_networks"]
all_devices_list = infra_config["devices"].keys()
container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()
network_dict = {}
coremark_avg = coremark_list = []
coremark_devices_all = {}

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "               Sanity check                   "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

"""
print "**************************** [Sanity] CPU allocation****************************"
for device in all_devices_list:
    vm_name = deployment_output[device]["host_vm_name"]
    host = container_vm[vm_name]["hostname_ip"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname = host, username = user, pkey = k)

    device_type = infra_config["devices"][device]["device_type"]

    if (device_type == "Pi2B"):
        path = "coremark_executables/coremark_2/coremark.exe"
    elif (device_type == "Pi3B"):
        path = "coremark_executables/coremark_2/coremark.exe"

    print "\n\nCopying coremark files to {0}".format(device)
    commands = [
    "sudo docker cp {0} {1}:/".format(path,device),
    "sudo docker cp c_coremark.py {0}:/".format(device)
    ]
    for command in commands:
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        print stdout.read()
        print stderr.read()

    time.sleep(1)
    print "Starting coremark in {0}".format(device)
    command = "sudo docker exec -i {0} python c_coremark.py &".format(device)

    stdin , stdout, stderr = c.exec_command(command)
    c.close()

print "Going to sleep"
time.sleep(1200)
"""

f_pi2b_delta = open("dump/sanity/f_pi2b_delta", "w")
f_pi3b_delta = open("dump/sanity/f_pi3b_delta", "w")
f_tx1_delta = open("dump/sanity/f_tx1_delta", "w")
f_si_delta  = open("dump/sanity/f_si_delta", "w")

f_pi2b = open("dump/sanity/f_pi2b", "w")
f_pi3b = open("dump/sanity/f_pi3b", "w")
f_tx1 = open("dump/sanity/f_tx1", "w")
f_si = open("dump/sanity/f_si", "w")
f_cm_all = open("dump/sanity/f_cm_all","w")

print "Collecting numbers"
for device in all_devices_list:
    cm_d = {}
    coremark= []
    vm_name = deployment_output[device]["host_vm_name"]
    host = container_vm[vm_name]["hostname_ip"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname = host, username = user, pkey = k)

    print "\n\nCollecting numbers in {0}".format(device)
    command = "sudo docker exec -i {0} cat results-coremark | grep \"CoreMark 1.0\" | awk '{{print $4}}'".format(device)
    stdin , stdout, stderr = c.exec_command(command)
    print stderr.read()

    observed_coremark = stdout.read()
    observed_coremark = observed_coremark.split("\n")
    observed_coremark.pop()
    for i in observed_coremark:
        coremark.append(float(i))
    coremark.sort()

    c_median = median(coremark)
    if len(coremark) != 0:
        c_avg = float(sum(coremark)) /float(len(coremark))
    else:
        c_avg = 0
        print "len(coremark) = 0"


    d_type = infra_config["devices"][device]["device_type"]
    expected_coremark = device_types[d_type]["coremark"]
    cm_d["device_type"] = d_type
    coremark_str = []
    for c_str in coremark:
        coremark_str.append(str(c_str))

    cm_d["coremark"] = coremark_str
    cm_d["n"] = len(coremark_str)
    cm_d["vm"] = vm_name
    cm_d["mean"] = str(c_avg)
    cm_d["median"] = str(c_median)

    coremark_devices_all[device] = cm_d
    for cm in coremark:
        f_cm_all.write(device+"\t"+d_type+"\t"+vm_name+"\t"+str(cm)+"\n")


    print "\ndevice - {0} \n  device_type = {1} \n  expected coremark = {2} observed coremark = {3}\n\n".format(device, d_type, expected_coremark, c_avg)

    delta = (float(c_avg) - float(expected_coremark)) / float(expected_coremark) * 100
    print delta

    if d_type == "Pi2B":
        f_pi2b_delta.write(str(delta)+"\n")
        f_pi2b.write(str(c_avg)+","+str(c_median)+"\n")
    elif d_type == "Pi3B":
        f_pi3b_delta.write(str(delta)+"\n")
        f_pi3b.write(str(c_avg)+","+str(c_median)+"\n")
    elif d_type == "TX1":
        f_tx1_delta.write(str(delta)+"\n")
        f_tx1.write(str(c_avg)+","+str(c_median)+"\n")
    elif d_type == "SI":
        f_si_delta.write(str(delta)+"\n")
        f_si.write(str(c_avg)+","+str(c_median)+"\n")

    c.close()

f_pi2b.close()
f_pi2b_delta.close()
f_pi3b.close()
f_pi3b_delta.close()

f_cm_all.close()
f_tx1.close()
f_tx1_delta.close()
f_si.close()
f_si_delta.close()

with open('dump/sanity/cm_device_all','w') as file:
    file.write(json.dumps(coremark_devices_all))


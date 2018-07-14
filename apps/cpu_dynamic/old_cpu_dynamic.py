import json
import time
import sys
import os
import docker
import math
import random

def device_down(devices,n):
    m = len(devices)
    device_down_count = int(math.ceil(n * p))
    if ((device_down_count > m) and (m != 0)):
        device_down_count = m
    elif (m == 0):
        sys.exit()

    current_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(current_time_epoch))
    print "\n Bringing down {0} devices with p = {1} current time = {2}".format(dev_type,p,current_time)
    device_down_list = random.sample(devices, device_down_count)
    print "\nRemoving these devices\n"
    print device_down_list

    for d in device_down_list:
        """
        vm_name = device_vm[d]
        host = container_vm[vm_name]["public_DNS"]
        user = container_vm[vm_name]["user"]
        key = container_vm[vm_name]["key_path"]
        k = paramiko.RSAKey.from_private_key_file(key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname = host, username = user, pkey = k)

        command = "docker stop {0}".format(d)
        stdin, stdout, stderr = c.exec_command(command)
        """
        devices.remove(d)

infra_config = json.load(open("../../config/infra_config.json"))
#device_vm = json.load(open('../../dump/infra/infra_device_vm.json'))
vm_config = json.load(open("../../config/vm_config.json"))
device_types = json.load(open("../../config/device_types.json"))
#edge_devices = json.load(open("../../dump/infra/infra_edge_devices.json"))
#fog_devices = json.load(open("../../dump/infra/infra_fog_devices.json"))

container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()

#dev_class = sys.argv[1]
#dev_type = sys.argv[2]

devices = []
if(dev_class == "edge"):
    mttf = int(device_types["edge_device_types"][dev_type]["mttf_sec"])
    p = float(device_types["edge_device_types"][dev_type]["probability_to_fail"])
    for e in edge_devices:
        if(infra_config["devices"]["Edge"][e]["device_type"] == dev_type):
            devices.append(e)
elif(dev_class == "fog"):
    mttf = int(device_types["fog_device_types"][dev_type]["mttf_sec"])
    p = float(device_types["fog_device_types"][dev_type]["probability_to_fail"])
    for e in edge_devices:
        if(infra_config["devices"]["Fog"][e]["device_type"] == dev_type):
            devices.append(e)


start_time_epoch = time.time()
start_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(start_time_epoch))
print "\nDevice - {0} start time =  [{1}] \n MTTF = {2} seconds \n Probability = {3}".format(dev_type, start_time, mttf, p)
print "List of {0} devices".format(dev_type)
print devices
print
n = len(devices)

while(True):
    current_time_epoch = time.time()
    diff = int (current_time_epoch - start_time_epoch)
    if(diff >= mttf):
        start_time_epoch = time.time()
        device_down(devices,n)


"""
for d in edge_devices:
    vm_name = device_vm[d]
    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname = host, username = user, pkey = k)

    command = "docker inspect {0} | grep Status | awk '{{print $2}}'  | sed 's/[\",]//g'".format(d)
    stdin, stdout, stderr = c.exec_command(command)
    status = stdout.read()
    edge_object_mapping[d] = status
"""


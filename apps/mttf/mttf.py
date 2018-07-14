import json
import time
import sys
import os
import docker
import math
import random
import paramiko

device_down_list = []

def device_down(devices,n,C):
    m = len(devices)
    if (m == 0):
        print "All the devices are down"
        return -1

    print "\n\n***control_interval***"
    current_time_epoch = time.time()
    current_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(current_time_epoch))
    print "start_time = {0} \ncurrent_time = {1} \ntime elapsed = {2} \nmttf = {3}".format(start_time,current_time,int(current_time_epoch - actual_start_time_epoch), mttf)
    for d in devices:
        r = random.randint(1,C)
        pivot = C * control_interval / mttf
        print "device = {0} pivot = {1} r = {2}".format(d,math.ceil(pivot), r)
        if (r > math.ceil(pivot)):
            continue
        print "\n Bringing down {0} device".format(d)
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
        device_down_list.append(d)
        devices.remove(d)
    print "device_down_list = {0}\n count = {1}\n".format(device_down_list, len(device_down_list))

infra_config = json.load(open("../../config/infra_config.json"))
print infra_config
device_vm = json.load(open('../../dump/infra/infra_device_vm.json'))
vm_config = json.load(open("../../config/vm_config.json"))
device_types = json.load(open("../../config/device_types.json"))
edge_devices = json.load(open("../../dump/infra/infra_edge_devices.json"))
fog_devices = json.load(open("../../dump/infra/infra_fog_devices.json"))

container_vm = vm_config["container_host_VM"]
container_vm_names = container_vm.keys()

dev_class = sys.argv[1]
dev_type = sys.argv[2]

devices = []
if(dev_class == "edge"):
    mttf = int(device_types["edge_device_types"][dev_type]["mttf_sec"])
    mttr = int(device_types["edge_device_types"][dev_type]["mttr_sec"])
    control_interval = int(device_types["edge_device_types"][dev_type]["control_interval"])
    constant = int(device_types["edge_device_types"][dev_type]["constant"])
    for e in edge_devices:
        print e
        if(infra_config["devices"]["Edge"][e]["device_type"] == dev_type):
            devices.append(e)
elif(dev_class == "fog"):
    mttf = int(device_types["fog_device_types"][dev_type]["mttf_sec"])
    mttr = int(device_types["fog_device_types"][dev_type]["mttr_sec"])
    control_interval = int(device_types["fog_device_types"][dev_type]["control_interval"])
    constant = int(device_types["edge_device_types"][dev_type]["constant"])
    for f in fog_devices:
        if(infra_config["devices"]["Fog"][f]["device_type"] == dev_type):
            devices.append(f)


start_time_epoch = time.time()
actual_start_time_epoch = start_time_epoch
start_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(start_time_epoch))
print "\nDevice - {0} start time =  [{1}] \n MTTF = {2} seconds \n".format(dev_type, start_time, mttf)
print "List of {0} devices".format(dev_type)
print devices
print
n = len(devices)

while(True):
    current_time_epoch = time.time()
    diff = int (current_time_epoch - start_time_epoch)
    if(diff >= control_interval):
        start_time_epoch = time.time()
        val = device_down(devices,n,constant)
        if (val == -1):
            break

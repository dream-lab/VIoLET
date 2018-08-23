import json
import time
import sys
import os
import math
import random
from datetime import datetime
import paramiko

def action_ci(devices):
    for d in devices:
        r = random.uniform(0.0, 1.0)
        #print "Device - {0} r - {1} p - {2}".format(d,r,probability)
        if r <= probability:
            cpu_cm = {}
            #print "Inside *IF*"
            coremark = random.uniform(coremark_min,coremark_max)
            #coremark = (coremark_min + coremark_max) / 2.0
            #coremark = coremark_min
            coremark = math.ceil(coremark)
            vm_name = deployment_output[d]["host_vm_name"]
            vm_type = vm_config["container_VM"][vm_name]["vm_type"]
            vm_coremark = vm_types[vm_type]["coremark"]
            vm_core_count = vm_types[vm_type]["core_count"]
            cpus_updated = float(coremark)/ float(vm_coremark) * float(vm_core_count)
            cpus_updated = float("{0:.2f}".format(cpus_updated))
            cpu_cm["cpus"] = cpus_updated
            cpu_cm["coremark"] = coremark

            host = container_vm[vm_name]["hostname_ip"]
            user = container_vm[vm_name]["user"]
            key = container_vm[vm_name]["key_path"]
            k = paramiko.RSAKey.from_private_key_file(key)
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(hostname = host, username = user, pkey = k)

            command = "sudo docker update --cpus={0} {1}".format(cpus_updated,d)
            stdin, stdout, stderr = c.exec_command(command,timeout=5)
            #print stdout.read()
            #print stderr.read()

            print "Device {0} updated [cpus = {1}, coremark = {2}]".format(d, cpus_updated, coremark)
            device_cpus_updated [d] = cpu_cm

    with open('../../dump/resource_dynamism/cpu_dynamism/device_cpus_updated_{0}.json'.format(d_type),'w') as file:
        file.write(json.dumps(device_cpus_updated))

infra_config = json.load(open("../../config/infra_config.json"))
vm_config = json.load(open("../../config/vm_config.json"))
device_types = json.load(open("../../config/device_types.json"))
vm_types = json.load(open("../../config/vm_types.json"))
deployment_json = json.load(open("../../config/deployment.json"))
deployment_output = json.load(open("../../dump/infra/deployment_output.json"))
all_devices_list = infra_config["devices"].keys()
container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()
device_cpus_updated = {}
d_type = sys.argv[1]
devices = []

cpu_var = float(device_types[d_type]["reliability"]["cpu_var_max"])
cpu_var_period = float(device_types[d_type]["reliability"]["cpu_var_period_sec"])
coremark_max = float(device_types[d_type]["coremark"])
coremark_min = coremark_max * (1 - cpu_var)
control_interval = float(deployment_json["control_interval_secs"])
probability = float(control_interval)/float(cpu_var_period)


for d in all_devices_list:
    if infra_config["devices"][d]["device_type"] == d_type:
        devices.append(d)

start_time_epoch = time.time()
start_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(start_time_epoch))
print "\nDevice type - {0} \n  start time =  [{1}] \n  cpu_var = {2} \n  cpu_var_period = {3} sec \n  coremark_max = {4}\n  coremark_min ={5}\n  control_interval = {6}\n  probability = {7}\n\n".format(d_type, start_time, cpu_var, cpu_var_period, coremark_max, coremark_min, control_interval, probability)
print "List of {0} devices".format(d_type)
print devices
print

while(True):
    current_time_epoch = time.time()
    diff = int (current_time_epoch - start_time_epoch)
    if(diff >= control_interval):
        print "\n\n**********Action time! [{0}]**********\n".format(time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(current_time_epoch)))
        start_time_epoch = time.time()
        action_ci(devices)

import json
import time
import sys
import os
import docker
import math
import random
import paramiko


infra_config = json.load(open("../../config/infra_config.json"))
device_vm = json.load(open('../../dump/infra/infra_device_vm.json'))
vm_config = json.load(open("../../config/vm_config.json"))
device_types = json.load(open("../../config/device_types.json"))
edge_devices = json.load(open("../../dump/infra/infra_edge_devices.json"))
fog_devices = json.load(open("../../dump/infra/infra_fog_devices.json"))

container_vm = vm_config["container_host_VM"]
container_vm_names = container_vm.keys()

device_networks = json.load(open("../../dump/infra/infra_device_networks.json"))
flag = sys.argv[1]
device = sys.argv[2]

vm_name = device_vm[device]
host = container_vm[vm_name]["public_DNS"]
user = container_vm[vm_name]["user"]
key = container_vm[vm_name]["key_path"]
k = paramiko.RSAKey.from_private_key_file(key)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(hostname = host, username = user, pkey = k)

d_net = device_networks[device]

if(flag == "disconnect"):
    for net in d_net:
        if (net == "violet_control_interface"):
            continue
        command = "sudo docker network disconnect {0} {1}".format(net,device)
        stdin, stdout, stderr = c.exec_command(command)
        print stdout.read()
        print stderr.read()

elif(flag == "connect"):
    for net in d_net:
        if (net == "violet_control_interface"):
            continue
        command = "sudo docker network connect {0} {1}".format(net,device)
        stdin, stdout, stderr = c.exec_command(command)
        print stdout.read()
        print stderr.read()

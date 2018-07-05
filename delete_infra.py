import os
import paramiko
import random
import time
import json
import threading
import sys
from datetime import datetime
from threading import Thread

startTime = datetime.now()


#Init Variables
infra_config = json.load(open("config/infra_config.json"))
private_networks_dict = json.load(open('dump/infra/infra_pvt.json'))
public_networks_dict = json.load(open('dump/infra/infra_pub.json'))
device_vm = json.load(open('dump/infra/infra_device_vm.json'))
device_ip = json.load(open('dump/infra/infra_device_ip.json'))
edge_devices = json.load(open('dump/infra/infra_edge_devices.json'))
fog_devices = json.load(open('dump/infra/infra_fog_devices.json'))
all_devices = json.load(open('dump/infra/all_devices_list.json'))
vm_config = json.load(open("config/vm_config.json"))
ip_device = {v: k for k, v in device_ip.iteritems()}

container_vm = vm_config["container_host_VM"]
container_vm_names = container_vm.keys()
private_networks = infra_config["private_networks"].keys()
public_networks = infra_config["public_networks"].keys()



print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "               Deleting Infra                  "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

#Delete containers
for vm in container_vm_names:
    print "Deleting Infra in {0}".format(vm)
    vm_name = vm
    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname = host, username = user, pkey = k)
    command = "sudo docker rm $(docker ps -a -q) --force"
    stdin , stdout, stderr = c.exec_command(command)
    print stdout.read()
    print stderr.read()
    c.close()

time.sleep(5)
#Delete networks
print "Deleting Networks"
vm_name = container_vm_names[0]
host = container_vm[vm_name]["public_DNS"]
user = container_vm[vm_name]["user"]
key = container_vm[vm_name]["key_path"]
k = paramiko.RSAKey.from_private_key_file(key)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

c.connect(hostname = host, username = user, pkey = k)

for p in private_networks:
    command = "sudo docker network rm {0}".format(p)
    stdin , stdout, stderr = c.exec_command(command)
    print stdout.read()
    print stderr.read()

for p in public_networks:
    command = "sudo docker network rm {0}".format(p)
    stdin , stdout, stderr = c.exec_command(command)
    print stdout.read()
    print stderr.read()

command = "sudo docker network rm violet_control_interface"
stdin , stdout, stderr = c.exec_command(command)
print stdout.read()
print stderr.read()
c.close()


print "{0}".format(datetime.now() - startTime)

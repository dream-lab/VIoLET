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
#private_networks_dict = json.load(open('dump/infra/infra_pvt.json'))
#public_networks_dict = json.load(open('dump/infra/infra_pub.json'))
#device_vm = json.load(open('dump/infra/infra_device_vm.json'))
#device_ip = json.load(open('dump/infra/infra_device_ip.json'))
#edge_devices = json.load(open('dump/infra/infra_edge_devices.json'))
#fog_devices = json.load(open('dump/infra/infra_fog_devices.json'))
#all_devices = json.load(open('dump/infra/all_devices_list.json'))
vm_config = json.load(open("config/vm_config.json"))
#deployment_output = json.load(open("dump/infra/deployment_output.json"))

#ip_device = {v: k for k, v in device_ip.iteritems()}

container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()
private_networks = infra_config["private_networks"].keys()
public_networks = infra_config["public_networks"].keys()
devices = infra_config["devices"].keys()

admin_ip = vm_config["admin_VM"]["VIoLET_admin"]["hostname_ip"]

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "               Deleting Infra                  "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

'''
for c_vm in container_vm:
    host = container_vm[c_vm]["hostname_ip"]
    user = container_vm[c_vm]["user"]
    key = container_vm[c_vm]["key_path"]
    commands = [
        "nohup ssh -i {0} {1}@{2} sudo pkill dockerd".format(key,user,host),
        "nohup ssh -i {0} {1}@{2} sudo /usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --cluster-advertise {2}:2375 --cluster-store consul://{3}:8500 &".format(key,user,host,admin_ip)
    ]
    for command in commands:
        print command
        os.system(command)
        time.sleep(2)
'''


#Delete containers
for vm_name in container_vm_names:
    #vm_name = deployment_output[device]["host_vm_name"]
    print "Deleting Infra in {0}".format(vm_name)
    host = container_vm[vm_name]["hostname_ip"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname = host, username = user, pkey = k)
    command = "sudo docker ps -a -q"
    stdin,stdout,stderr = c.exec_command(command)

    for device in stdout.read().split():
        print device
        command = "sudo docker container rm -f {0}".format(device)
        #print command
        stdin , stdout, stderr = c.exec_command(command)
        #print stdout.read()
        #print stderr.read()
    c.close()

time.sleep(1)
#Delete networks
print "Deleting Networks"
vm_name = container_vm_names[0]
host = container_vm[vm_name]["hostname_ip"]
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

#command = "sudo docker network rm violet_control_interface"
#stdin , stdout, stderr = c.exec_command(command)
#print stdout.read()
#print stderr.read()
c.close()

'''
for c_vm in container_vm:
    host = container_vm[c_vm]["hostname_ip"]
    user = container_vm[c_vm]["user"]
    key = container_vm[c_vm]["key_path"]
    commands = [
        "nohup ssh -i {0} {1}@{2} sudo pkill dockerd".format(key,user,host),
        "nohup ssh -i {0} {1}@{2} sudo /usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --cluster-advertise {2}:2375 --cluster-store consul://{3}:8500 &".format(key,user,host,admin_ip)
    ]
    for command in commands:
        print command
        os.system(command)
'''

print "{0}".format(datetime.now() - startTime)

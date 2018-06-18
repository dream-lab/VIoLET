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


#Init Variables
infra_config = json.load(open("config/infra_config.json"))
device_types = json.load(open("config/device_types.json"))

private_networks_dict = json.load(open('dump/infra/infra_pvt.json'))
public_networks_dict = json.load(open('dump/infra/infra_pub.json'))
device_vm = json.load(open('dump/infra/infra_device_vm.json'))
device_ip = json.load(open('dump/infra/infra_device_ip.json'))
edge_devices = json.load(open('dump/infra/infra_edge_devices.json'))
fog_devices = json.load(open('dump/infra/infra_fog_devices.json'))

coremark_devices_all = {}

vm_config = json.load(open("config/vm_config.json"))
ip_device = {v: k for k, v in device_ip.iteritems()}

container_vm = vm_config["container_host_VM"]
container_vm_names = container_vm.keys()

coremark_avg = coremark_list = []

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "               Starting docker                   "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print



for vm_name in container_vm_names:
    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname = host, username = user, pkey = k)

    stdin, stdout, stderr = c.exec_command(command,timeout=5)
    print stdout.read()
    print stderr.read()

    c.close()

#print "{0} - {1}".format(datetime.now() - startTime)

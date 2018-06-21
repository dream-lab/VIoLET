
import os
import paramiko
import random
import time
import json
import threading
import sys
from datetime import datetime
from threading import Thread

private_networks_dict = json.load(open('../../dump/infra/infra_pvt.json'))
device_networks_dict = json.load(open('../../dump/infra/infra_device_networks.json'))
device_vm = json.load(open('../../dump/infra/infra_device_vm.json'))
vm_config = json.load(open("../../config/vm_config.json"))
container_vm = vm_config["container_host_VM"]


pub_list_txt = open('publisher_list.txt', 'r')


print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "               Sanity check                   "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

pub_list = pub_list_txt.readlines()

print len(pub_list)

pub_file_list = []
sub_file_list = []
lat_file_list = []

tmp_dir = "tmp"

os.system("mkdir tmp")

for pl in pub_list:
    device, file_key = pl.split()
    network_name = device_networks_dict[device][0]
    fog = private_networks_dict[network_name]["gw"]
    print fog
    vm_name = device_vm[device]
    tmp_fog_device_dir = tmp_dir + "/" + fog + "/" + device
    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect(hostname = host, username = user, pkey = k)

    pub_file = "pub_" + file_key
    sub_file = "sub_" + file_key
    lat_file = "latency_" + file_key

    pub_file_list.append(pub_file)
    sub_file_list.append(sub_file)
    lat_file_list.append(lat_file)

    commands = [
            "sudo docker cp {0}:{1} .".format(device, pub_file),
            "sudo docker cp {0}:{1} .".format(device, sub_file),
            "sudo docker cp {0}:{1} .".format(device, lat_file)
            ]

    for command in commands:
        stdin, stdout, stderr = c.exec_command(command)

    c.close()

    time.sleep(0.2)

    commands = [
            "mkdir -p {0}".format(tmp_fog_device_dir),
            "scp -i {0} {1}@{2}:{3} {4}".format(key, user, host, pub_file, tmp_fog_device_dir),
            "scp -i {0} {1}@{2}:{3} {4}".format(key, user, host, sub_file, tmp_fog_device_dir),
            "scp -i {0} {1}@{2}:{3} {4}".format(key, user, host, lat_file, tmp_fog_device_dir),
            "diff {0}/{1} {0}/{2}".format(tmp_fog_device_dir, pub_file, sub_file),
            "wc -l {0}".format(tmp_fog_device_dir + "/" + lat_file)
            ]

    for command in commands:
        os.system(command)



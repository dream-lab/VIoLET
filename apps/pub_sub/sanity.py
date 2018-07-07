
import os
import paramiko
import random
import time
import json
import threading
import sys
from datetime import datetime
from threading import Thread


'''
private_networks_dict = json.load(open('../../dump/infra/infra_pvt.json'))
fog_devices = json.load(open('../../dump/infra/infra_fog_devices.json'))
device_networks_dict = json.load(open('../../dump/infra/infra_device_networks.json'))
device_vm = json.load(open('../../dump/infra/infra_device_vm.json'))
vm_config = json.load(open("../../config/vm_config.json"))
container_vm = vm_config["container_host_VM"]
container_vm_names = container_vm.keys()
'''

infra_config = json.load(open("../../config/infra_config.json"))
deployment_output = json.load(open("../../dump/infra/deployment_output.json"))
all_device_list = deployment_output.keys()
private_networks_dict = infra_config["private_networks"]
public_networks_dict = infra_config["public_networks"]
vm_config = json.load(open("../../config/vm_config.json"))

networks = []

latency_dict = {}

for n in private_networks_dict.keys():
    networks.append(n)
    latency_dict[n] = private_networks_dict[n]["latency_ms"]

for n in public_networks_dict.keys():
    networks.append(n)
    latency_dict[n] = public_networks_dict[n]["latency_ms"]

print latency_dict

container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()


pub_sub_data = "data"
path = "VIoLET/pub_sub"


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


for pl in pub_list:
    device, file_key, network = pl.split()
    if network == "private":
        network_name = deployment_output[device]["private_networks"].keys()
        print network_name[0]
    else:
        network_name = deployment_output[device]["public_networks"].keys()
        print network_name[0]

    vm_name = deployment_output[device]["host_vm_name"]
    tmp_fog_dir = tmp_dir + "/" + network_name[0]
    tmp_fog_device_dir = tmp_fog_dir + "/" + device
    host = container_vm[vm_name]["hostname_ip"]
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
        "sudo docker cp {0}:{1}/{2}/{3} .".format(device,path,pub_sub_data,pub_file),
        "sudo docker cp {0}:{1}/{2}/{3} .".format(device,path,pub_sub_data,sub_file),
        "sudo docker cp {0}:{1}/{2}/{3} .".format(device,path,pub_sub_data,lat_file)
    ]

    for command in commands:
        print command
        stdin, stdout, stderr = c.exec_command(command)
        print stderr.read()
    c.close()

    time.sleep(0.2)

    commands = [
            "mkdir -p {0}".format(tmp_fog_device_dir),
            "scp -i {0} {1}@{2}:{3} {4}".format(key, user, host, pub_file, tmp_fog_device_dir),
            "scp -i {0} {1}@{2}:{3} {4}".format(key, user, host, sub_file, tmp_fog_device_dir),
            "scp -i {0} {1}@{2}:{3} {4}".format(key, user, host, lat_file, tmp_fog_device_dir),
            #"diff {0}/{1} {0}/{2}".format(tmp_fog_device_dir, pub_file, sub_file),
            "wc -l {0}".format(tmp_fog_device_dir + "/" + lat_file),
            "cat {0}/{1} >> {2}/{3}".format(tmp_fog_device_dir, lat_file, tmp_dir, network_name[0]+"_latency.txt")
            ]

    for command in commands:
        print command
        os.system(command)

#for lat_file in lat_file_list:
#    commands = [
#            "cat {0}/{1} >> latency.txt".format(tmp_fog_device_dir, lat_file)
#            ]
#    for command in commands:
#        os.system(command)

networks.sort()

for network in networks:
    f = open(tmp_dir + "/" + network + "_latency.txt", "r")
    expected = float(latency_dict[network]) * 4
    latencies = f.readlines()
    f.close()
    d = open(tmp_dir + "/" + network + "_deviation.txt", "w")
    for lat in latencies:
        dev = (((float(lat) * 1000) - expected) / expected) * 100
        d.write(str(dev) + "\n")

    d.close()




plot_in_file = "latency_deviation.txt"

command = "paste -d ',' "

for network in networks:
    print network
    command += tmp_dir + "/" + network + "_deviation.txt" + " "

command += " > {0}".format(plot_in_file)

os.system(command)

plot_out_file = "latency_deviation"

command = 'python ../../vPlot.py {0} {1} "'.format(plot_in_file, plot_out_file)

for network in networks:
    print network
    command += network + ","

#command = command[:len(command) - 1]

command += '" "Latency Deviation % " "Networks"'

os.system(command)


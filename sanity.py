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

private_network = sys.argv[1]

#Init Variables
private_networks_dict = json.load(open('dump/infra/infra_pvt.json'))
public_networks_dict = json.load(open('dump/infra/infra_pub.json'))
device_vm = json.load(open('dump/infra/infra_device_vm.json'))
device_ip = json.load(open('dump/infra/infra_device_ip.json'))
vm_config = json.load(open("config/vm_config.json"))
ip_device = {v: k for k, v in device_ip.iteritems()}

container_vm = vm_config["container_host_VM"]
container_vm_names = container_vm.keys()

print container_vm
print
print container_vm_names
#Create AWS connection
#key_path = "/home/centos/CIBO-CentOS.pem"
#user = "centos"
#k = paramiko.RSAKey.from_private_key_file(key_path)
#c = paramiko.SSHClient()
#c.set_missing_host_key_policy(paramiko.AutoAddPolicy())


print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "               Sanity check                   "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

iperf = {}
print "--------------------------------------"
print "    {0} ".format(private_network)
print "--------------------------------------"
print "Expected BW - {0}Mbps      Expected Latency -{1}ms".format(private_networks_dict[private_network]["bw"],private_networks_dict[private_network]["latency"])
iperf["expected bw"] = private_networks_dict[private_network]["bw"]
iperf["expected latency"] = private_networks_dict[private_network]["latency"]

num_edge_dev = len(private_networks_dict[private_network]["conn_dev"])
num_iperf = int(num_edge_dev * 0.5)
iperf_numbers = {}

for i in range(1,num_iperf+1):
    index1 = index2 = 0
    iperf_i = {}
    while True:
        index1 = random.randint(0,num_edge_dev - 1)
        index2 = random.randint(0,num_edge_dev - 1)
        if index1 != index2:
            break
    device1 = private_networks_dict[private_network]["conn_dev"][index1]
    device2 = private_networks_dict[private_network]["conn_dev"][index2]
    iperf_i["device-1"] = device1
    iperf_i["device-2"] = device2

    vm_name = device_vm[device1]
    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect(hostname = host, username = user, pkey = k)
    #vm = device_vm[device1]
    #c.connect(hostname = vm, username = user, pkey = k)
    command = "sudo docker exec -i {0} iperf3 -s -p 4343".format(device1)
    stdin , stdout, stderr = c.exec_command(command)
    ip = device_ip[device1]
    c.close()

    #vm = device_vm[device2]
    #c.connect(hostname = vm, username = user, pkey = k)
    vm_name = device_vm[device2]
    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect(hostname = host, username = user, pkey = k)
    command = "sudo docker exec -i {0} iperf3 -c {1} -p 4343 | grep sender | awk '{{print $7}}' &".format(device2,ip)
    stdin , stdout, stderr = c.exec_command(command)
    bw = stdout.read()
    bw = bw.replace(' ','')[:-1]
    print "{0} <-> {1} [{2}Mbps]".format(device1, device2, bw)
    iperf_i["bw"] = bw
    iperf_numbers[i]= iperf_i
    c.close()

iperf["iperf_numbers"] = iperf_numbers

num_edge_dev = len(private_networks_dict[private_network]["conn_dev"])
num_ping = int(num_edge_dev * 2)
latency_numbers = {}
for i in range(1,num_ping+1):
    index1 = index2 = 0
    while True:
        index1 = random.randint(0,num_edge_dev - 1)
        index2 = random.randint(0,num_edge_dev - 1)
        if index1 != index2:
            break
    latency_i = {}
    device1 = private_networks_dict[private_network]["conn_dev"][index1]
    device2 = private_networks_dict[private_network]["conn_dev"][index2]

    latency_i["device 1"] = device1
    latency_i["device 2"] = device2
    #vm = device_vm[device1]
    #c.connect(hostname = vm, username = user, pkey = k)
    vm_name = device_vm[device1]
    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect(hostname = host, username = user, pkey = k)
    command = "sudo docker exec -i {0} ip route | grep default | awk '{{print $3}}'".format(device1)
    stdin , stdout, stderr = c.exec_command(command)
    ip = stdout.read()
    ip = ip.replace(' ','')[:-1]
    gw = ip_device[ip]
    iperf["gw"] = gw
    reachable = {}
    print
    print "{0}  (default gw - {1})".format(device1,gw)
    command = "sudo docker exec -i {0} fping -e -c2 -t500 {1} | grep bytes".format(device1,device_ip[device2])
    stdin , stdout, stderr = c.exec_command(command)
    output = stdout.read()
    print output
    print "after"
    output = output.split("\n")
    print output
    if(len(output)>1):
        output = output[1].split(" ")
        print output[5]
        if(output[5]):
            reachable[device2]=device_ip[device2]
            print "  {0} -> {1}  latency={2}ms (rtt)".format(device1, device2, output[5])
            latency_i["latency"]= output[5]
        latency_numbers[i] = latency_i
    else:
        print "PROBLEM! {0} <-> {1}".format(device1,device2)
    c.close()

iperf["latency_numbers"] = latency_numbers

for device in private_networks_dict[private_network]["conn_dev"]:
    with open("dump/sanity/sanity_{0}".format(private_network), 'w') as file:
     file.write(json.dumps(iperf))

print "{0} - {1}".format(private_network,datetime.now() - startTime)

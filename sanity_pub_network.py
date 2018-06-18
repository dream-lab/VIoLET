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

public_network = sys.argv[1]

#Init Variables
private_networks_dict = json.load(open('dump/infra/infra_pvt.json'))
public_networks_dict = json.load(open('dump/infra/infra_pub.json'))
device_vm = json.load(open('dump/infra/infra_device_vm.json'))
device_ip = json.load(open('dump/infra/infra_device_ip.json'))
edge_devices = json.load(open('dump/infra/infra_edge_devices.json'))
fog_devices = json.load(open('dump/infra/infra_fog_devices.json'))
eth_port_map = json.load(open('dump/infra/eth_port_map.json'))

vm_config = json.load(open("config/vm_config.json"))
ip_device = {v: k for k, v in device_ip.iteritems()}

container_vm = vm_config["container_host_VM"]
container_vm_names = container_vm.keys()


print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "               Sanity check                   "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

iperf = {}
print "**************************** [Sanity] Bandwidth, gateway, latency allocation****************************"
print "--------------------------------------"
print "    {0} ".format(public_network)
print "--------------------------------------"
print "Expected BW - {0}Mbps      Expected Latency -{1}ms".format(public_networks_dict[public_network]["bw"],public_networks_dict[public_network]["latency"])
iperf["expected bw"] = public_networks_dict[public_network]["bw"]
iperf["expected latency"] = public_networks_dict[public_network]["latency"]

num_fog_dev = len(public_networks_dict[public_network]["conn_dev"])
num_iperf = int(num_fog_dev)
iperf_numbers = {}

for i in range(1,num_iperf+1):
    index1 = index2 = 0
    iperf_i = {}
    while True:
        index1 = random.randint(0,num_fog_dev - 1)
        index2 = random.randint(0,num_fog_dev - 1)
        if index1 != index2:
            break
    device1 = public_networks_dict[public_network]["conn_dev"][index1]
    device2 = public_networks_dict[public_network]["conn_dev"][index2]
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

    command = "sudo docker exec -i {0} iperf3 -s -p 4343".format(device1)
    stdin , stdout, stderr = c.exec_command(command)
    eth_port = eth_port_map[device1][public_network]

    command = "sudo docker exec -i {0} ip a | grep eth{1} | awk 'FNR == 2 {{print $2}}'".format(device1,eth_port)
    stdin, stdout, stderr = c.exec_command(command)

    output = stdout.read()
    ip = output.replace(' ','')[:-4]

    print "{0} [{1}] - {2}".format(device1,ip,device2)

    c.close()

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



print "Latency"
num_fog_dev = len(public_networks_dict[public_network]["conn_dev"])
num_ping = int(num_fog_dev * 2)
latency_numbers = {}
for i in range(1,num_ping+1):
    index1 = index2 = 0
    while True:
        index1 = random.randint(0,num_fog_dev - 1)
        index2 = random.randint(0,num_fog_dev - 1)
        if index1 != index2:
            break
    latency_i = {}
    device1 = public_networks_dict[public_network]["conn_dev"][index1]
    device2 = public_networks_dict[public_network]["conn_dev"][index2]

    latency_i["device 1"] = device1
    latency_i["device 2"] = device2
    vm_name = device_vm[device2]
    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect(hostname = host, username = user, pkey = k)

    reachable = {}

    eth_port = eth_port_map[device2][public_network]
    #print "device1 = {0} device2 = {1} eth_port (for device1) = {3} eth_port (for device2) = {2}".format(device1,device2,eth_port,eth_port_map[device1][public_network])
    command = "sudo docker exec -i {0} ip a | grep eth{1} | awk 'FNR == 2 {{print $2}}'".format(device2,eth_port)
    stdin, stdout, stderr = c.exec_command(command)
    time.sleep(1)
    output = stdout.read()
    #print output
    #print "Error"
    #print stderr.read()
    time.sleep(1)

    ip = output.replace(' ','')[:-4]
    if not ip:
        continue

    #print "{0} pinging {1} [{2}]".format(device1,device2, ip)
    c.close()

    vm_name = device_vm[device1]
    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect(hostname = host, username = user, pkey = k)


    command = "sudo docker exec -i {0} fping -e -c2 -t500 {1} | grep bytes".format(device1,ip)
    stdin , stdout, stderr = c.exec_command(command)
    output = stdout.read()
    output = output.split("\n")
    if(len(output)>1):
        output = output[1].split(" ")
        if(output[5]):
            reachable[device2]=device_ip[device2]
            print "{0} -> {1}  latency={2}ms (rtt)".format(device1, device2, output[5])
            latency_i["latency"]= output[5]
        latency_numbers[i] = latency_i
    else:
        print "ERROR! {0} <-> {1} are either not connected or not in same network".format(device1,device2)
    c.close()

iperf["latency_numbers"] = latency_numbers

for device in public_networks_dict[public_network]["conn_dev"]:
    with open("dump/sanity/sanity_{0}".format(public_network), 'w') as file:
     file.write(json.dumps(iperf))

print "{0} - {1}".format(public_network,datetime.now() - startTime)

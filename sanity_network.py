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

network_type = sys.argv[1]
network = sys.argv[2]

infra_config = json.load(open("config/infra_config.json"))
vm_config = json.load(open("config/vm_config.json"))
vm_types = json.load(open("config/vm_types.json"))
sensors =  json.load(open("config/sensor_types.json"))
deployment =  json.load(open("config/deployment.json"))
device_types =  json.load(open("config/device_types.json"))
deployment_output = json.load(open("dump/infra/deployment_output.json"))
eth_ip_dict = json.load(open("dump/infra/eth_ip.json"))

private_networks_dict = infra_config["private_networks"]
public_networks_dict = infra_config["public_networks"]
all_devices_list = infra_config["devices"].keys()
container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()
network_dict = {}

if network_type == "pvt":
    network_dict = private_networks_dict
elif network_type == "pub":
    network_dict = public_networks_dict

#private_networks_dict = json.load(open('dump/infra/infra_pvt.json'))
#public_networks_dict = json.load(open('dump/infra/infra_pub.json'))
#device_vm = json.load(open('dump/infra/infra_device_vm.json'))
#device_ip = json.load(open('dump/infra/infra_device_ip.json'))
#edge_devices = json.load(open('dump/infra/infra_edge_devices.json'))
#fog_devices = json.load(open('dump/infra/infra_fog_devices.json'))
#eth_port_map = json.load(open('dump/infra/eth_port_map.json'))

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "               Sanity check                   "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

iperf = {}
print "**************************** [Sanity] Bandwidth, gateway, latency allocation****************************"
print "-------------------------------------------------------------"
print "{0}\n".format(network)
print "Expected BW - {0}Mbps\nExpected Latency -{1}ms".format(network_dict[network]["bandwidth_mbps"],network_dict[network]["latency_ms"])
print "-------------------------------------------------------------\n"

iperf["expected_bandwidth_mbps"] = network_dict[network]["bandwidth_mbps"]
iperf["expected_latency_ms"] = network_dict[network]["latency_ms"]


#Bandwidth
print "*****BANDWIDTH*****"
num_connected_devices = len(network_dict[network]["devices"])
num_iperf_pairs = int(num_connected_devices * 0.5)
iperf_numbers = {}

for i in range(1,num_iperf_pairs+1):
    index1 = index2 = 0
    iperf_i = {}
    while True:
        index1 = random.randint(0,num_connected_devices - 1)
        index2 = random.randint(0,num_connected_devices - 1)
        if index1 != index2:
            break
    device1 = network_dict[network]["devices"][index1]
    device2 = network_dict[network]["devices"][index2]
    iperf_i["device_1"] = device1
    iperf_i["device_2"] = device2

    #Start iperf on device1 as a server
    vm_name = deployment_output[device1]["host_vm_name"]
    host = container_vm[vm_name]["hostname_ip"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname = host, username = user, pkey = k)

    command = "sudo docker exec -i {0} iperf3 -s -p 4343".format(device1)
    stdin , stdout, stderr = c.exec_command(command)
    if network_type == "pvt":
        ip = deployment_output[device1]["private_networks"][network]
    elif network_type == "pub":
        ip = deployment_output[device1]["public_networks"][network]

    c.close()

    #Start iperf on device2 as a client and record the numbers
    vm_name = deployment_output[device2]["host_vm_name"]
    host = container_vm[vm_name]["hostname_ip"]
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
    print "\t{0} <-> {1} [{2}Mbps]".format(device1, device2, bw)
    iperf_i["observed_bandwidth_mbps"] = bw
    iperf_numbers[i]= iperf_i
    c.close()

iperf["bandwidth_numbers"] = iperf_numbers

#Latency
print "*****LATENCY*****"
num_connected_devices = len(network_dict[network]["devices"])
num_ping_pairs = int(num_connected_devices * 2)
latency_numbers = {}
for i in range(1,num_ping_pairs+1):
    index1 = index2 = 0
    while True:
        index1 = random.randint(0,num_connected_devices - 1)
        index2 = random.randint(0,num_connected_devices - 1)
        if index1 != index2:
            break
    latency_i = {}
    device1 = network_dict[network]["devices"][index1]
    device2 = network_dict[network]["devices"][index2]

    latency_i["device_1"] = device1
    latency_i["device_2"] = device2
    vm_name = deployment_output[device1]["host_vm_name"]
    host = container_vm[vm_name]["hostname_ip"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname = host, username = user, pkey = k)

    """
    command = "sudo docker exec -i {0} ip route | grep default | awk '{{print $3}}'".format(device1)
    stdin , stdout, stderr = c.exec_command(command)
    ip = stdout.read()
    ip = ip.replace(' ','')[:-1]
    gw = ip_device[ip]
    iperf["gw"] = gw
    print
    print "{0}  (default gw - {1})".format(device1,gw)
    """
    if network_type == "pvt":
        ip = deployment_output[device2]["private_networks"][network]
    elif network_type == "pub":
        ip = deployment_output[device2]["public_networks"][network]

    command = "sudo docker exec -i {0} fping -e -c2 -t500 {1} | grep bytes".format(device1,ip)
    stdin , stdout, stderr = c.exec_command(command,timeout = 5)
    output = stdout.read()
    output = output.split("\n")
    if(len(output)>1):
        output = output[1].split(" ")
        if(output[5]):
            print "{0} -> {1} [{2}ms (rtt)]".format(device1, device2, output[5])
            latency_i["observed_latency_ms"]= output[5]
        latency_numbers[i] = latency_i
    else:
        print "ERROR! {0} <-> {1} are either not connected or not in same network".format(device1,device2)
    c.close()

iperf["latency_numbers"] = latency_numbers

with open("dump/sanity/sanity_{0}".format(network),'w') as file:
    file.write(json.dumps(iperf))

print "{0} - {1}".format(network,datetime.now() - startTime)

#for device in private_networks_dict[network]["conn_dev"]:
#    with open("dump/sanity/sanity_{0}".format(network), 'w') as file:
#     file.write(json.dumps(iperf))

import os
import paramiko
import random
import time
import json
from datetime import datetime
from threading import Thread

startTime = datetime.now()

infra_config = json.load(open("config/infra_config.json"))
vm_config = json.load(open("config/vm_config.json"))
vm_types = json.load(open("config/vm_types.json"))
sensors =  json.load(open("config/sensor_types.json"))
deployment =  json.load(open("config/deployment.json"))
device_types =  json.load(open("config/device_types.json"))
partitions = json.load(open('dump/metis/metis_partitions.json'))

private_networks_dict = infra_config["private_networks"]
public_networks_dict = infra_config["public_networks"]
public_global_network_dict = infra_config["public_global_network"]
all_devices_list = infra_config["devices"].keys()

deployment_output = {}
eth_ip_dict = {}
container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()

log_file = open("violet_log","w")

print
print
print ("**************************************************************************")
print ("                            DEPLOYING VIoLET                              ")
print ("**************************************************************************")
print
print

log_file.write("\n\n\n****************************************     DEPLOYING VIOLET       ****************************************\n")
"""
print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "             Copy data to other VMs            "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

for i in range(1,len(hosts)):
    for data in data_path_copy_vm:
        os.system("scp -i {0} {1} {2}@{3}:/home/{2}".format(key_path, data, user, hosts[i]))
"""


print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "          Creating overlay networks            "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print
log_file.write("\n\n\n**************************************** CREATING OVERLAY NETWORKS ****************************************\n")

host = container_vm[container_vm_names[0]]["hostname_ip"]
user = container_vm[container_vm_names[0]]["user"]
key = container_vm[container_vm_names[0]]["key_path"]
k = paramiko.RSAKey.from_private_key_file(key)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect( hostname = host, username = user, pkey = k)

print "Creating public_global_network"
ip_range = public_global_network_dict["ip_range"]
subnet = public_global_network_dict["subnet"]
command = "sudo docker network create -d overlay --ip-range={0} --subnet={1} public_global_network".format(ip_range,subnet)

stdin , stdout, stderr = c.exec_command(command)
log_file.write(stderr.read()+"\n")
log_file.write(stdout.read()+"\n")

public_networks = public_networks_dict.keys()
for i in public_networks:
        ip_range = public_networks_dict[i]["ip_range"]
        subnet = public_networks_dict[i]["subnet"]
        command = "sudo docker network create -d overlay --ip-range={0} --subnet={1} {2}".format(ip_range,subnet,i)
        print "Creating {0} network".format(str(i))
        log_file.write("Creating {0} network\n".format(str(i)))
        stdin , stdout, stderr = c.exec_command(command)
        log_file.write(stderr.read()+"\n")
        log_file.write(stdout.read()+"\n")

private_networks = private_networks_dict.keys()
for i in private_networks:
        ip_range = private_networks_dict[i]["ip_range"]
        subnet = private_networks_dict[i]["subnet"]
        command = "sudo docker network create -d overlay --ip-range={0} --subnet={1} {2}".format(ip_range,subnet,i)
        print "Creating {0} network".format(str(i))
        log_file.write("Creating {0} network \n".format(str(i)))
        stdin , stdout, stderr = c.exec_command(command)
        log_file.write(stderr.read()+"\n")
        log_file.write(stdout.read()+"\n")
c.close()

docker0_bridge_dict = {}
for vm in container_vm_names:
    host = container_vm[vm]["hostname_ip"]
    user = container_vm[vm]["user"]
    key = container_vm[vm]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect( hostname = host, username = user, pkey = k)

    command = "sudo docker network inspect bridge | grep \"Gateway\" | awk '{{print $2}}'"
    stdin , stdout, stderr = c.exec_command(command)
    output = stdout.read()
    output = output.split("\n")[0]
    output = output.replace("\"","")
    ip_range = output[:-3]
    docker0_bridge_dict[vm] = ip_range

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "      Creating containers (IoT devices)        "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

log_file.write("\n\n\n****************************************     CREATING CONTAINERS     ****************************************\n")

#CREATE DEVICES
for d in all_devices_list:
    device_output = {}
    device_type = infra_config["devices"][d]["device_type"]

    #cpus has to be picked automatically once the initial steps are automated.
    ########################
    if device_type == "Pi2B":
        cpus = 0.96
    elif device_type == "Pi3B":
        cpus = 1.48
    elif device_type == "TX1":
        cpus = 2.84
    elif device_type == "SI":
        cpus = 8.21
    ########################

    container_OS = device_types[device_type]["docker_image"]
    container_host_mount_path = device_types[device_type]["host_mount"]
    memory_mb = device_types[device_type]["memory_mb"]
    disk_mb = device_types[device_type]["disk_mb"]
    nic_out_bw_mbps = device_types[device_type]["nic_out_bw_mbps"]
    device_relibality_params =  device_types[device_type]["reliability"]

    vm_index = int(partitions[d])
    vm_name = container_vm_names[vm_index]
    vm_mount_path = vm_types[vm_config["container_VM"][vm_name]["vm_type"]]["shared_mount"]
    host = container_vm[vm_name]["hostname_ip"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect( hostname = host, username = user, pkey = k)

    commands = ["sudo docker run --ulimit nofile=500:500  -i -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v {0}:{1} --cpus={2}  --privileged --cap-add=NET_ADMIN --cap-add=NET_RAW --hostname {3} --name {3} {4} > /dev/null &".format(container_host_mount_path,vm_mount_path,cpus,d,container_OS)]

    print "Creating {0} in {1} {2}".format(d,vm_name,host)
    log_file.write("\n\nCreating {0} in {1}\n".format(d,vm_name))
    for command in commands:
        log_file.write(command+"\n")
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        log_file.write(stdout.read()+"\n")
        log_file.write(stderr.read()+"\n")

    device_output["host_vm_name"] = vm_name
    device_output["host_vm_ip"] = host
    deployment_output[d] = device_output
    print deployment_output[d]
    c.close()


print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "      Establishing network connectivity        "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print
log_file.write("\n\n\n***************************************ESTABLISHNING NETWORK CONNECTIVITY***************************************\n")


for d in all_devices_list:
    eth_ip_dict[d] = {}
    deployment_output[d]["private_networks"] = {}
    deployment_output[d]["public_networks"] = {}
    deployment_output[d]["sensors"] = {}



print "-------------------------"
print "Creating private networks"
print "-------------------------"

log_file.write("\n\n++++++++++ CREATING PRIVATE NETWORKS  ++++++++++\n")


private_network = private_networks_dict.keys()
for i in range(len(private_networks_dict)):

    #To begin with, connect gateway device to the network and do the necessary NATing
    gw = private_networks_dict[private_network[i]]["gateway"]
    vm_name = deployment_output[gw]["host_vm_name"]
    host = container_vm[vm_name]["hostname_ip"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname = host, username = user, pkey = k)

    #Connect the gateway to the private network
    command = "sudo docker network connect {0} {1}".format(private_network[i],gw)
    print "Connecting {0} to {1}".format(gw,private_network[i])
    log_file.write("Connecting {0} to {1} \n".format(gw,private_network[i]))
    stdin, stdout, stderr = c.exec_command(command)
    log_file.write("\n {0} \n {1}\n".format(stdout.read(), stderr.read()))

    #Determine the eth number for gateway device connected to docker_d0
    ip_range = docker0_bridge_dict[vm_name]
    device_ip = {}
    command = "sudo docker exec -i {0} ip a | grep {1} | awk '{{print $2}} {{print $7}}'".format(gw,ip_range)
    stdin, stdout, stderr = c.exec_command(command)
    output = stdout.read()
    output = output.split("\n")
    device_ip["IP"] = output[0].split("/")[0]
    device_ip["eth"] = output[1]
    eth_ip_dict[gw]["docker_d0_bridge"] = device_ip
    deployment_output[gw]["public_networks"]["docker_d0_bridge"] = device_ip["IP"]

    #Determine the eth number for gateway device connected to the private network
    ip_range_pvt = private_networks_dict[private_network[i]]["ip_range"]
    ip_range_pvt = ip_range_pvt.split("/")[0][:-1]
    device_ip = {}
    command = "sudo docker exec -i {0} ip a | grep {1} | awk '{{print $2}} {{print $7}}'".format(gw,ip_range_pvt)
    stdin, stdout, stderr = c.exec_command(command)
    output = stdout.read()
    output = output.split("\n")
    device_ip["IP"] = output[0].split("/")[0]
    device_ip["eth"] = output[1]
    eth_ip_dict[gw][private_network[i]] = device_ip
    deployment_output[gw]["private_networks"][private_network[i]] = device_ip["IP"]

    #NATing on the gateway device to allow the traffic from private devices to the internet.
    commands = [
    "sudo docker exec -i {0} service iptables start".format(gw),
    "sudo docker exec -i {0} iptables -t nat -A POSTROUTING -o {1} -j MASQUERADE".format(gw,eth_ip_dict[gw]["docker_d0_bridge"]["eth"]),
    "sudo docker exec -i {0} iptables -A FORWARD -i {1} -o {2} -m state --state RELATED,ESTABLISHED -j ACCEPT".format(gw,eth_ip_dict[gw]["docker_d0_bridge"]["eth"], eth_ip_dict[gw][private_network[i]]["eth"]),
    "sudo docker exec -i {0} iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT".format(gw,eth_ip_dict[gw][private_network[i]]["eth"],eth_ip_dict[gw]["docker_d0_bridge"]["eth"]),
    "sudo docker exec -i {0} iptables -D INPUT -j REJECT --reject-with icmp-host-prohibited".format(gw),
    "sudo docker exec -i {0} iptables -D FORWARD -j REJECT --reject-with icmp-host-prohibited".format(gw)
    ]
    for command in commands:
        stdin, stdout, stderr = c.exec_command(command)

    #TC rules for gateway to private devices interaction to limit BW and Latency.
    commands = [
    "sudo docker exec -i {0} tc qdisc add dev {1} handle 1: root htb default 11".format(gw, eth_ip_dict[gw][private_network[i]]["eth"]),
    "sudo docker exec -i {0} tc class add dev {1} parent 1: classid 1:1 htb rate {2}Mbps".format(gw, eth_ip_dict[gw][private_network[i]]["eth"], private_networks_dict[private_network[i]]["bandwidth_mbps"]),
    "sudo docker exec -i {0} tc class add dev {1} parent 1:1 classid 1:11 htb rate {2}Mbit".format(gw, eth_ip_dict[gw][private_network[i]]["eth"], private_networks_dict[private_network[i]]["bandwidth_mbps"]),
    "sudo docker exec -i {0} tc qdisc add dev {1} parent 1:11 handle 10: netem delay {2}ms".format(gw, eth_ip_dict[gw][private_network[i]]["eth"], float( private_networks_dict[private_network[i]]["latency_ms"]))
    ]
    log_file.write("Setting TC rules\n")
    for command in commands:
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        log_file.write(command+"\n")
        log_file.write(stdout.read()+"\n")
        log_file.write(stderr.read()+"\n")

    #Connect the gateway to the public_global_network
    command = "sudo docker network connect {0} {1}".format("public_global_network",gw)
    log_file.write("Connecting {0} to {1} \n".format(gw,"public_global_network"))
    stdin, stdout, stderr = c.exec_command(command)
    log_file.write("\n {0} \n {1}\n".format(stdout.read(), stderr.read()))

    #Determine the eth number for gateway device connected to public_global_network.
    ip_range = public_global_network_dict["ip_range"]
    ip_range = ip_range.split("/")[0][:-1]
    device_ip = {}
    command = "sudo docker exec -i {0} ip a | grep {1} | awk '{{print $2}} {{print $7}}'".format(gw,ip_range)
    stdin, stdout, stderr = c.exec_command(command)
    output = stdout.read()
    output = output.split("\n")
    device_ip["IP"] = output[0].split("/")[0]
    device_ip["eth"] = output[1]
    eth_ip_dict[gw]["public_global_network"] = device_ip
    deployment_output[gw]["public_global_network"] = device_ip["IP"]


    #NATing on the gateway device to allow the traffic from private devices to reach other public devices through public_global_network.
    commands = [
    "sudo docker exec -i {0} iptables -t nat -A POSTROUTING -o {1} -j MASQUERADE".format(gw,eth_ip_dict[gw]["public_global_network"]["eth"]),
    "sudo docker exec -i {0} iptables -A FORWARD -i {1} -o {2} -m state --state RELATED,ESTABLISHED -j ACCEPT".format(gw,eth_ip_dict[gw]["public_global_network"]["eth"], eth_ip_dict[gw][private_network[i]]["eth"]),
    "sudo docker exec -i {0} iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT".format(gw,eth_ip_dict[gw][private_network[i]]["eth"],eth_ip_dict[gw]["public_global_network"]["eth"]),
    "sudo docker exec -i {0} iptables -D INPUT -j REJECT --reject-with icmp-host-prohibited".format(gw),
    "sudo docker exec -i {0} iptables -D FORWARD -j REJECT --reject-with icmp-host-prohibited".format(gw)
    ]
    for command in commands:
        stdin, stdout, stderr = c.exec_command(command)


    #TC rules for private devices and public devices interaction to limit BW and Latency.
    commands = [
    "sudo docker exec -i {0} tc qdisc add dev {1} handle 1: root htb default 11".format(gw, eth_ip_dict[gw]["public_global_network"]["eth"]),
    "sudo docker exec -i {0} tc class add dev {1} parent 1: classid 1:1 htb rate {2}Mbps".format(gw, eth_ip_dict[gw]["public_global_network"]["eth"], public_global_network_dict["bandwidth_mbps"]),
    "sudo docker exec -i {0} tc class add dev {1} parent 1:1 classid 1:11 htb rate {2}Mbit".format(gw, eth_ip_dict[gw]["public_global_network"]["eth"], public_global_network_dict["bandwidth_mbps"]),
    "sudo docker exec -i {0} tc qdisc add dev {1} parent 1:11 handle 10: netem delay {2}ms".format(gw, eth_ip_dict[gw]["public_global_network"]["eth"], float( public_global_network_dict["latency_ms"]))
    ]
    log_file.write("Setting TC rules\n")
    for command in commands:
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        log_file.write(command+"\n")
        log_file.write(stdout.read()+"\n")
        log_file.write(stderr.read()+"\n")
    c.close()

    #Now connect the private_devices to the private network
    for j in range(len(private_networks_dict[private_network[i]]["devices"])):
        device = private_networks_dict[private_network[i]]["devices"][j]
        vm_name = deployment_output[device]["host_vm_name"]
        host = container_vm[vm_name]["hostname_ip"]
        user = container_vm[vm_name]["user"]
        key = container_vm[vm_name]["key_path"]
        k = paramiko.RSAKey.from_private_key_file(key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname = host, username = user, pkey = k)

        #Connect the private device to the private network.
        print "Connecting {0} to {1}".format(device, private_network[i])
        log_file.write("Connecting {0} to {1}\n".format(device, private_network[i]))
        command = "sudo docker network connect {0} {1}".format(private_network[i],device)
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        #time.sleep(0.5)
        log_file.write("\n {0} \n {1}\n".format(stdout.read(), stderr.read()))

        #By default containers are attached to the bridge network, disconnect it.
        command = "sudo docker network disconnect bridge {0}".format(device)
        c.exec_command(command,timeout=5)
        command = "sudo docker network disconnect docker_gwbridge {0}".format(device)
        c.exec_command(command,timeout=5)

        #Determine the eth number for private network connected to the private device
        device_ip = {}
        command = "sudo docker exec -i {0} ip a | grep {1} | awk '{{print $2}} {{print $7}}'".format(device,ip_range_pvt)
        stdin, stdout, stderr = c.exec_command(command)
        output = stdout.read()
        output = output.split("\n")
        device_ip["IP"] = output[0].split("/")[0]
        device_ip["eth"] = output[1]
        eth_ip_dict[device][private_network[i]] = device_ip
        deployment_output[device]["private_networks"][private_network[i]] = device_ip["IP"]


        #Apply the TC rules
        commands = [
        "sudo docker exec -i {0} tc qdisc add dev {1} handle 1: root htb default 11".format(device, eth_ip_dict[device][private_network[i]]["eth"]),
        "sudo docker exec -i {0} tc class add dev {1} parent 1: classid 1:1 htb rate {2}Mbps".format(device, eth_ip_dict[device][private_network[i]]["eth"], private_networks_dict[private_network[i]]["bandwidth_mbps"]),
        "sudo docker exec -i {0} tc class add dev {1} parent 1:1 classid 1:11 htb rate {2}Mbit".format(device, eth_ip_dict[device][private_network[i]]["eth"], private_networks_dict[private_network[i]]["bandwidth_mbps"]),
        "sudo docker exec -i {0} tc qdisc add dev {1} parent 1:11 handle 10: netem delay {2}ms".format(device, eth_ip_dict[device][private_network[i]]["eth"], float( private_networks_dict[private_network[i]]["latency_ms"]))
        ]
        log_file.write("Setting TC rules\n")
        for command in commands:
            stdin, stdout, stderr = c.exec_command(command,timeout=5)
            log_file.write(command+"\n")
            log_file.write(stdout.read()+"\n")
            log_file.write(stderr.read()+"\n")
            #time.sleep(0.2)

        #Remove the default gateway and add the above gateway device in "ip route"
        command = "sudo docker exec -i {0} ip route | grep default | awk '{{print $3}}'".format(device)
        stdin , stdout, stderr = c.exec_command(command,timeout=5)
        log_file.write(command+"\n")
        log_file.write(stdout.read()+"\n")
        log_file.write(stderr.read()+"\n")
        def_gw = stdout.read()
        def_gw = def_gw.replace(' ','')[:-1].upper()
        log_file.write("(Default GW) Changing to -> {1} \n".format(def_gw,eth_ip_dict[gw][private_network[i]]["IP"]))
        command = "sudo docker exec -i {0} route del default gw {1}".format(device,def_gw)
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        command = "sudo docker exec -i {0} route add default gw {1}".format(device,eth_ip_dict[gw][private_network[i]]["IP"])
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        command = "sudo docker exec -i {0} ip a | grep {1} | awk 'FNR == 2 {{print $2}}'".format(device,eth_ip_dict[device][private_network[i]]["eth"])
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        #time.sleep(.5)
        ip = stdout.read()
        ip = ip.replace(' ','')[:-4]
        print "Device({0}) IP - {1}".format(device,ip)
        c.close()

print "------------------------"
print "Creating public networks"
print "------------------------"


log_file.write("\n\n++++++++++ CREATING PUBLIC NETWORKS  ++++++++++\n")

public_network = public_networks_dict.keys()
for i in range(len(public_networks_dict)):
    for j in range(len(public_networks_dict[public_network[i]]["devices"])):
        device = public_networks_dict[public_network[i]]["devices"][j]
        vm_name = deployment_output[device]["host_vm_name"]
        host = container_vm[vm_name]["hostname_ip"]
        user = container_vm[vm_name]["user"]
        key = container_vm[vm_name]["key_path"]
        k = paramiko.RSAKey.from_private_key_file(key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        c.connect(hostname = host, username = user, pkey = k)

        command = "sudo docker network connect {0} {1}".format(public_network[i],device)
        print "Connecting {0} to {1}".format(device, public_network[i])
        log_file.write("Connecting {0} to {1} \n".format(device, public_network[i]))
        stdin , stdout, stderr = c.exec_command(command,timeout=5)
        #time.sleep(0.5)
        log_file.write("\n {0} \n {1}\n".format(stdout.read(), stderr.read()))

        command = "sudo docker network disconnect docker_gwbridge {0}".format(device)
        c.exec_command(command,timeout=5)

        ip_range = public_networks_dict[public_network[i]]["ip_range"]
        ip_range = ip_range.split("/")[0][:-1]
        device_ip = {}
        command = "sudo docker exec -i {0} ip a | grep {1} | awk '{{print $2}} {{print $7}}'".format(device,ip_range)
        stdin, stdout, stderr = c.exec_command(command)
        output = stdout.read()
        output = output.split("\n")
        device_ip["IP"] = output[0].split("/")[0]
        device_ip["eth"] = output[1]
        eth_ip_dict[device][public_network[i]] = device_ip
        deployment_output[device]["public_networks"][public_network[i]] = device_ip["IP"]

        commands = [
        "sudo docker exec -i {0} tc qdisc add dev {1} handle 1: root htb default 11".format(device, eth_ip_dict[device][public_network[i]]["eth"]),
        "sudo docker exec -i {0} tc class add dev {1} parent 1: classid 1:1 htb rate {2}Mbps".format(device, eth_ip_dict[device][public_network[i]]["eth"], public_networks_dict[public_network[i]]["bandwidth_mbps"]),
        "sudo docker exec -i {0} tc class add dev {1} parent 1:1 classid 1:11 htb rate {2}Mbit".format(device, eth_ip_dict[device][public_network[i]]["eth"], public_networks_dict[public_network[i]]["bandwidth_mbps"]),
        "sudo docker exec -i {0} tc qdisc add dev {1} parent 1:11 handle 10: netem delay {2}ms".format(device, eth_ip_dict[device][public_network[i]]["eth"], float( public_networks_dict[public_network[i]]["latency_ms"]))
        ]

        log_file.write("Setting TC rules\n")
        for command in commands:
            stdin, stdout, stderr = c.exec_command(command,timeout=5)
            log_file.write(command+"\n")
            log_file.write(stdout.read()+"\n")
            log_file.write(stderr.read()+"\n")
        c.close()


print eth_ip_dict
print deployment_output

"""
print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "           Create sensors                      "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print
log_file.write("\n\n\n****************************************      CREATING SENSORS      ****************************************\n")

edge_count = len(edge_devices)
bundle = "datagen.tar.gz"

devices_with_sensors = {}

for e in edge_devices:
    print "Creating sensors for device - {0}".format(e)
    log_file.write("Creating sensors for device - {0} \n".format(e))
    s = []
    sensor_index = 1
    e_sensors = infra_config["devices"]["Edge"][e]["sensors"].keys()

    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect(hostname = host, username = user, pkey = k)

    command = "sudo docker exec -i {0} mkdir sensors".format(e)
    stdin , stdout, stderr = c.exec_command(command)
    for e_sensor in e_sensors:
        num_sensors = infra_config["devices"]["Edge"][e]["sensors"][e_sensor]
        for i in range(1,int(num_sensors)+1):
            sensor_file_name = e+"_"+e_sensor+"_"+str(sensor_index)
            s.append(sensor_file_name)
            command = "sudo docker exec -i {0} touch sensors/{1}".format(e,sensor_file_name)
            stdin , stdout, stderr = c.exec_command(command)
            sensor_index += 1
    devices_with_sensors[e]=s
"""

with open('dump/infra/deployment_output.json','w') as file:
    file.write(json.dumps(deployment_output))
with open('dump/infra/eth_ip.json','w') as file:
    file.write(json.dumps(eth_ip_dict))
log_file.close()
print datetime.now() - startTime



"""


with open('dump/infra/infra_fog_devices.json','w') as file:
    file.write(json.dumps(fog_devices))
with open('dump/infra/infra_edge_devices.json','w') as file:
    file.write(json.dumps(edge_devices))
with open('dump/infra/infra_devices_with_sensors.json','w') as file:
    file.write(json.dumps(devices_with_sensors))
with open('dump/infra/eth_port_map.json','w') as file:
    file.write(json.dumps(eth_port_map))
#with open('dump/infra/infra_device_networks.json','w') as file:
#    file.write(json.dumps(device_networks))


with open('dump/infra/infra_devices.json', 'w') as file:
     file.write(json.dumps(devices))
with open('dump/infra/infra_pvt.json', 'w') as file:
     file.write(json.dumps(private_networks_dict))
with open('dump/infra/infra_pub.json', 'w') as file:
     file.write(json.dumps(public_networks_dict))

"""

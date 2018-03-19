import os
import paramiko
import random
import time
import json
from datetime import datetime
from threading import Thread

startTime = datetime.now()

#Init Variables
hosts = []

device_vm = {}
device_ip = {}
edge_device = [None]*1000

#Init Variables
devices = json.load(open('dump/topo-devices'))
num_devices = len(devices)
private_networks_dict = json.load(open('dump/topo-pvt'))
public_networks_dict = json.load(open('dump/topo-pub'))
fog_device = json.load(open('dump/topo-fog-devices'))
edge_device = json.load(open('dump/topo-edge-devices'))
#partitions = json.load(open('dump/algo-partitions'))
partitions = {}


#Create AWS connection
key_path = ""
user=""
k = paramiko.RSAKey.from_private_key_file(key_path)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())


print
print
print ("**************************************************************************")
print ("                            DEPLOYING CIBO                                ")
print ("**************************************************************************")
print
print

#Create Network Bridges
print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "          Creating overlay networks            "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

public_networks = public_networks_dict.keys()
c.connect( hostname = hosts[1], username = user, pkey = k )
command = "sudo docker network create -d overlay {0}".format(str(public_networks[0]))

print "Creating {0} network".format(str(public_networks[0]))
stdin , stdout, stderr = c.exec_command(command)
print stdout.read()

private_networks = private_networks_dict.keys()
for i in private_networks:
        command = "sudo docker network create -d overlay {0}".format(str(i))
        print "Creating {0} network".format(str(i))
        stdin , stdout, stderr = c.exec_command(command)
        print stdout.read()
c.close()

#Create Containers
print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "      Creating containers (IoT devices)        "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

for i in range(num_devices):
    cpus = ""
    commands = ["sudo docker run --ulimit nofile=50000:50000  -i -v /sys/fs/cgroup:/sys/fs/cgroup:ro --cpus={1}  --privileged --cap-add=NET_ADMIN --cap-add=NET_RAW --hostname {0} --name {0} centos_systemd > /dev/null &".format(devices[i],cpus)]
    metis = partitions[devices[i]]
    j = int(metis)+1 # 0 is Admin VM
    print hosts[j]
    print "Creating {0} in {1} \n {2}".format(devices[i],j,hosts[j])
    device_vm[devices[i]] = hosts[j]
    c.connect( hostname = hosts[j], username = user, pkey = k )
    for command in commands:
        print command
        stdin, stdout, stderr = c.exec_command(command)
        print stdout.read()
        print stderr.read()
    device=devices[i]

#Establish Network Connectivity
print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "      Establishing network connectivity        "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print


print "-------------------------"
print "Creating private networks"
print "-------------------------"

private_network = private_networks_dict.keys()
for i in range(len(private_networks_dict)):
    gw = private_networks_dict[private_network[i]]["gw"]
    vm = device_vm[gw]
    command = "sudo docker network connect {0} {1}".format(private_network[i],gw)
    c.connect( hostname = vm, username = user, pkey = k )
    print "Connecting {0} to {1}".format(gw,private_network[i])
    stdin, stdout, stderr = c.exec_command(command)

    command = "sudo docker exec -i {0} ip a | grep eth1 | awk 'FNR == 2 {{print $2}}'".format(gw)
    stdin, stdout, stderr = c.exec_command(command)
    ip = stdout.read()
    gw_ip = ip.replace(' ','')[:-4]
    device_ip[gw] = gw_ip

    commands = ["sudo docker exec -i {0} service iptables start".format(gw),"sudo docker exec -i {0} iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE".format(gw), "sudo docker exec -i {0} iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT".format(gw), "sudo docker exec -i {0} iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT".format(gw),"sudo docker exec -i {0} iptables -D INPUT -j REJECT --reject-with icmp-host-prohibited".format(gw),"sudo docker exec -i {0} iptables -D FORWARD -j REJECT --reject-with icmp-host-prohibited".format(gw)]
    for command in commands:
        stdin, stdout, stderr = c.exec_command(command)
    c.close()

    for j in range(len(private_networks_dict[private_network[i]]["conn_dev"])):
        device = private_networks_dict[private_network[i]]["conn_dev"][j]
        edge_device.append(device)
        vm = device_vm[device]
        command = "sudo docker network connect {0} {1}".format(private_network[i],device)
        c.connect( hostname = vm, username = user, pkey = k )
        print "Connecting {0} to {1}".format(device, private_network[i])
        c.exec_command(command)
        command = "sudo docker network disconnect bridge {0}".format(device)
        c.exec_command(command)
        command = "sudo docker network disconnect docker_gwbridge {0}".format(device)
        c.exec_command(command)
        commands =["sudo docker exec -i {0} tc qdisc add dev eth1 handle 1: root htb default 11".format(device),"sudo docker exec -i {0} tc class add dev eth1 parent 1: classid 1:1 htb rate {1}Mbps".format(device, private_networks_dict[private_network[i]]["bw"]),"sudo docker exec -i {0} tc class add dev eth1 parent 1:1 classid 1:11 htb rate {1}Mbit".format(device,private_networks_dict[private_network[i]]["bw"]),"sudo docker exec -i {0} tc qdisc add dev eth1 parent 1:11 handle 10: netem delay {1}ms".format(device,int( private_networks_dict[private_network[i]]["latency"]))]
        print "Setting TC rules"
        for command in commands:
            stdin, stdout, stderr = c.exec_command(command)
            print command
            print stdout.read()
            print stderr.read()
            time.sleep(0.4)
        command = "sudo docker exec -i {0} ip route | grep default | awk '{{print $3}}'".format(device)
        stdin , stdout, stderr = c.exec_command(command)
        print command
        print stdout.read()
        print stderr.read()

        def_gw = stdout.read()
        def_gw = def_gw.replace(' ','')[:-1].upper()
        print "{0} to -> {1}".format(def_gw,gw_ip)
        command = "sudo docker exec -i {0} route del default gw {1}".format(device,def_gw)
        stdin, stdout, stderr = c.exec_command(command)
        command = "sudo docker exec -i {0} route add default gw {1}".format(device,gw_ip)
        stdin, stdout, stderr = c.exec_command(command)
        command = "sudo docker exec -i {0} ip a | grep eth1 | awk 'FNR == 2 {{print $2}}'".format(device)
        stdin, stdout, stderr = c.exec_command(command)
        ip = stdout.read()
        ip = ip.replace(' ','')[:-4]
        device_ip[device]=ip
        c.close()

print "------------------------"
print "Creating public networks"
print "------------------------"

public_network = public_networks_dict.keys()
for i in range(len(public_networks_dict)):
    for j in range(len(public_networks_dict[public_network[i]]["conn_dev"])):
        device = public_networks_dict[public_network[i]]["conn_dev"][j]
        vm = device_vm[device]
        command = "sudo docker network connect {} {}".format(public_network[i],device)
        c.connect( hostname = vm, username = user, pkey = k )
        print "Connecting {0} to {1}".format(device, public_network[i])
        stdin , stdout, stderr = c.exec_command(command)
        c.close()


with open('dump/infra-hosts', 'w') as file:
     file.write(json.dumps(hosts))
with open('dump/infra-device-vm', 'w') as file:
     file.write(json.dumps(device_vm))
with open('dump/infra-device-ip', 'w') as file:
     file.write(json.dumps(device_ip))
with open('dump/infra-devices', 'w') as file:
     file.write(json.dumps(devices))
with open('dump/infra-pvt', 'w') as file:
     file.write(json.dumps(private_networks_dict))
with open('dump/infra-pub', 'w') as file:
     file.write(json.dumps(public_networks_dict))
with open('dump/infra-fog-devices','w') as file:
    file.write(json.dumps(fog_device))
edge_device = list(set(edge_device))
with open('dump/infra-edge-devices','w') as file:
    file.write(json.dumps(edge_device))

print device_ip
print device_vm
print datetime.now() - startTime

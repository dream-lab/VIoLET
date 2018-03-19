import os
import paramiko
import random
import time
import json
from datetime import datetime
from threading import Thread

startTime = datetime.now()

#Init Variables
hosts = [
"ec2-18-218-52-187.us-east-2.compute.amazonaws.com",
"ec2-18-222-57-93.us-east-2.compute.amazonaws.com"
]
device_vm = {}
device_ip = {}
infra_config = json.load(open("infra-config.json"))
edge_devices = infra_config["devices"]["Edge"].keys()
fog_devices = infra_config["devices"]["Fog"].keys()
devices = fog_devices + edge_devices
private_networks_dict = infra_config["private_networks"]
public_networks_dict = infra_config["public_networks"]
partitions = json.load(open('dump/algo-partitions'))
data_path_copy_vm = ["/home/centos/VIoLET/datagen.tar.gz"]


#CREATE AWS CONNECTION
key_path = "/home/centos/CIBO-CentOS.pem"
user="centos"
k = paramiko.RSAKey.from_private_key_file(key_path)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print
print
print ("**************************************************************************")
print ("                            DEPLOYING VIoLET                              ")
print ("**************************************************************************")
print
print

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "             Copy data to other VMs            "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

for i in range(1,len(hosts)):
    for data in data_path_copy_vm:
        os.system("scp -i {0} {1} {2}@{3}:/home/{2}".format(key_path, data, user, hosts[i]))

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
print stderr.read()

private_networks = private_networks_dict.keys()
for i in private_networks:
        command = "sudo docker network create -d overlay {0}".format(str(i))
        print "Creating {0} network".format(str(i))
        stdin , stdout, stderr = c.exec_command(command)
        print stderr.read()
        print stdout.read()
c.close()

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "      Creating containers (IoT devices)        "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

#CREATE FOG DEVICES
for f in fog_devices:
    print "CHANGE THE CPUS in INFRA later!!"
    device_type = infra_config["devices"]["Fog"][f]["device_type"]
    cpus = infra_config["fog_device_types"][device_type]["cpus"]
    commands = ["sudo docker run --ulimit nofile=50000:50000  -i -v /sys/fs/cgroup:/sys/fs/cgroup:ro --cpus={1}  --privileged --cap-add=NET_ADMIN --cap-add=NET_RAW --hostname {0} --name {0} centos_systemd > /dev/null &".format(f,cpus)]
    metis = partitions[f]
    index = int(metis)+1 #0 is Admin VM
    index = 1 #test
    device_vm[f] = hosts[index]
    c.connect( hostname = hosts[index], username = user, pkey = k )
    for command in commands:
        print command
        stdin, stdout, stderr = c.exec_command(command)
        print stdout.read()
        print stderr.read()
    c.close()

#CREATE EDGE DEVICES
for e in edge_devices:
    device_type = infra_config["devices"]["Edge"][e]["device_type"]
    cpus = infra_config["edge_device_types"][device_type]["cpus"]
    commands = ["sudo docker run --ulimit nofile=50000:50000  -i -v /sys/fs/cgroup:/sys/fs/cgroup:ro --cpus={1}  --privileged --cap-add=NET_ADMIN --cap-add=NET_RAW --hostname {0} --name {0} centos_systemd > /dev/null &".format(e,cpus)]
    metis = partitions[e]
    index = int(metis)+1 # 0 is Admin VM
    index = 1 #test
    print "Creating {0} in {1} \n {2}".format(e,index,hosts[index])
    device_vm[e] = hosts[index]
    c.connect( hostname = hosts[index], username = user, pkey = k )
    for command in commands:
        print command
        stdin, stdout, stderr = c.exec_command(command)
        print stdout.read()
        print stderr.read()
    c.close()

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
            time.sleep(0.2)
        command = "sudo docker exec -i {0} ip route | grep default | awk '{{print $3}}'".format(device)
        stdin , stdout, stderr = c.exec_command(command)
        print command
        print stdout.read()
        print stderr.read()

        def_gw = stdout.read()
        def_gw = def_gw.replace(' ','')[:-1].upper()
        print "(Default GW) Changing to -> {1}".format(def_gw,gw_ip)
        command = "sudo docker exec -i {0} route del default gw {1}".format(device,def_gw)
        stdin, stdout, stderr = c.exec_command(command)
        command = "sudo docker exec -i {0} route add default gw {1}".format(device,gw_ip)
        stdin, stdout, stderr = c.exec_command(command)
        command = "sudo docker exec -i {0} ip a | grep eth1 | awk 'FNR == 2 {{print $2}}'".format(device)
        stdin, stdout, stderr = c.exec_command(command)
        ip = stdout.read()
        ip = ip.replace(' ','')[:-4]
        device_ip[device]=ip
        command = "sudo docker exec -i {0} ip a".format(device)
        stdin, stdout, stderr = c.exec_command(command)
        print  "@@@@@@@@@@@@@@@@+++++++++++++++++++++@@@@@@@@@@@@@@@@@@@"
        print stdout.read()
        command = "sudo docker exec -i {0} ip route".format(device)
        stdin, stdout, stderr = c.exec_command(command)
        print stdout.read()
        print  "@@@@@@@@@@@@@@@@+++++++++++++++++++++@@@@@@@@@@@@@@@@@@"
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

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "           Create sensors                      "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

edge_count = len(edge_devices)
bundle = "datagen.tar.gz"

devices_with_sensors = {}

for e in edge_devices:
    s = []
    sensor_index = 1
    e_sensors = infra_config["devices"]["Edge"][e]["sensors"].keys()
    vm = device_vm[e]
    c.connect( hostname = vm, username = user, pkey = k )
    command = "sudo docker exec -i {0} mkdir sensors".format(e)
    stdin , stdout, stderr = c.exec_command(command)
    print stdout.read()
    print stderr.read()
    for e_sensor in e_sensors:
        num_sensors = infra_config["devices"]["Edge"][e]["sensors"][e_sensor]
        for i in range(1,int(num_sensors)+1):
            sensor_file_name = e+"_"+e_sensor+"_"+str(sensor_index)
            s.append(sensor_file_name)
            command = "sudo docker exec -i {0} touch sensors/{1}".format(e,sensor_file_name)
            stdin , stdout, stderr = c.exec_command(command)
            print stdout.read()
            print stderr.read()
            sensor_index += 1
    devices_with_sensors[e]=s

print "\n{0}\n".format(devices_with_sensors)

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
    file.write(json.dumps(fog_devices))
with open('dump/infra-edge-devices','w') as file:
    file.write(json.dumps(edge_devices))
with open('dump/infra-devices-with-sensors','w') as file:
    file.write(json.dumps(devices_with_sensors))


print device_ip
print device_vm
print datetime.now() - startTime

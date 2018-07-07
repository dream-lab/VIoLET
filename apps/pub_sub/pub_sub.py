import os
import sys
import string
import numpy as np
import paramiko
import random
import time
import json
import thread
import threading
from datetime import datetime
from threading import Thread

startTime = datetime.now()



#Init Variables
#hosts = json.load(open('../../dump/infra-hosts'))
#devices = json.load(open('../../dump/infra/infra_devices.json'))
infra_config = json.load(open("../../config/infra_config.json"))
deployment_output = json.load(open("../../dump/infra/deployment_output.json"))
all_device_list = deployment_output.keys()
private_networks_dict = infra_config["private_networks"]
public_networks_dict = infra_config["public_networks"]
#device_vm = json.load(open('../../dump/infra/infra_device_vm.json'))
#device_ip = json.load(open('../../dump/infra/infra_device_ip.json'))
#cloud_device = json.load(open('dump/infra-cloud-devices'))
#fog_device = json.load(open('../../dump/infra/infra_fog_devices.json'))
#ip_device = {v: k for k, v in device_ip.iteritems()}
#edge_device = json.load(open('../../dump/infra/infra_edge_devices.json'))
#infra_devices_with_sensors = json.load(open('../../dump/infra/infra_devices_with_sensors.json'))
vm_config = json.load(open("../../config/vm_config.json"))
#fog_sensor_link = json.load(open("../../dump/infra/infra_fog_sensor_link.json"))



fog_device = []

for d in all_device_list:
    if "Fog" in d:
        fog_device.append(d)

print fog_device

container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()


#pub_sub_tar = "scripts.tar.gz"
pub_sub = "scripts"
pub_sub_data = "data"
path = "VIoLET/pub_sub"

num_msgs = sys.argv[1]

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "                  PUB - SUB                    "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "             Copy data to other VMs            "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print


for i in range(len(container_vm_names)):
    key_path = container_vm[container_vm_names[i]]["key_path"]
    user = container_vm[container_vm_names[i]]["user"]
    host = container_vm[container_vm_names[i]]["hostname_ip"]
    os.system("scp -r -i {0} {1} {2}@{3}:/home/{2}".format(key_path, pub_sub, user, host))



print "Binding Broker address to Mosquitto....."

for fog in fog_device:
    vm_name = deployment_output[fog]["host_vm_name"]
    host = container_vm[vm_name]["hostname_ip"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect(hostname = host, username = user, pkey = k)

    nw_name_list = deployment_output[fog]["private_networks"].keys()
    fog_ip = deployment_output[fog]["private_networks"][nw_name_list[0]]

    commands = [
        "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(fog,path,pub_sub_data),
        "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(fog,path,pub_sub),
        "sudo docker cp -a {0} {1}:{2}".format(pub_sub,fog,path),
        "sudo docker exec -i {0} python {1}/{2}/mqtt.py {3}".format(fog,path,pub_sub,fog_ip),
        "sudo docker exec -i {0} systemctl start mosquitto".format(fog)
    ]
    for command in commands:
        print command
        stdin , stdout, stderr = c.exec_command(command)
        print stderr.read(),stdout.read()
    c.close()



pf = open("publisher_list.txt", "w")

for n in private_networks_dict:
    #total = len(private_networks_dict[n]["conn_dev"])
    #print "number of edge devices"
    #print total
    #cnt = 0
    fog = private_networks_dict[n]["gateway"]
    nw_name_list = deployment_output[fog]["private_networks"].keys()
    fog_ip = deployment_output[fog]["private_networks"][nw_name_list[0]]

    device_list = private_networks_dict[n]["devices"]
    sensor_link_list = []
    for device in device_list:
        sensors_list = deployment_output[device]["sensors"]
        for sensor in sensors_list:
            for link in sensor["links"]:
                sensor_link_list.append(link)

    #print sensor_link_list


    while len(device_list) >= 2:
        devices = random.sample(device_list,2)
        print "Devices --> ",devices
        topic = ''.join(random.choice(string.ascii_lowercase) for _ in range(32))
        print "Topic --> " + topic
        sensor_link = random.choice(sensor_link_list)
        print "sensor_link --> " + sensor_link
        print
        cmd = [
            "python {0}/{1}/subscribe.py {2} {3}".format(path,pub_sub,topic,fog_ip),
            "python {0}/{1}/publish.py {2} {3} {4} {5}".format(path,pub_sub,topic,fog_ip,sensor_link,num_msgs)
        ]

        #print command
        i=0
        for device in devices:
            vm_name = deployment_output[device]["host_vm_name"]
            host = container_vm[vm_name]["hostname_ip"]
            user = container_vm[vm_name]["user"]
            key = container_vm[vm_name]["key_path"]
            k = paramiko.RSAKey.from_private_key_file(key)
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(hostname = host, username = user, pkey = k)

            commands = [
                "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(device,path,pub_sub_data),
                "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(device,path,pub_sub),
                "sudo docker cp -a {0} {1}:{2}".format(pub_sub,device,path,pub_sub),
                "sudo docker exec -id {0} {1}".format(device,cmd[i])
            ]
            if i == 1:
                pf.write(device + " " + topic + "\n")

            for command in commands:
                print command
                stdin,stdout,stderr = c.exec_command(command)
                print stderr.read(),stdout.read()
            c.close()

            i=1
            #time.sleep(2)

        for device in devices:
            device_list.remove(device)

        sensor_link_list.remove(sensor_link)

    if len(device_list) == 1:
        device = device_list[0]
        print "Devices --> ",device
        topic = ''.join(random.choice(string.ascii_lowercase) for _ in range(32))
        print "Topic --> " + topic
        sensor_link = random.choice(sensor_link_list)
        print "sensor_link --> " + sensor_link
        print


        vm_name = deployment_output[device]["host_vm_name"]
        host = container_vm[vm_name]["hostname_ip"]
        user = container_vm[vm_name]["user"]
        key = container_vm[vm_name]["key_path"]
        k = paramiko.RSAKey.from_private_key_file(key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname = host, username = user, pkey = k)

        commands = [
            "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(device,path,pub_sub_data),
            "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(device,path,pub_sub),
            "sudo docker cp -a {0} {1}:{2}".format(pub_sub,device,path,pub_sub),
            "sudo docker exec -id {0} python {1}/{2}/subscribe.py {3} {4}".format(device,path,pub_sub,topic,fog_ip),
            "sudo docker exec -id {0} python {1}/{2}/publish.py {3} {4} {5} {6}".format(device,path,pub_sub,topic,fog_ip,sensor_link,num_msgs)
        ]
        pf.write(device + " " + topic + "\n")

        for command in commands:
            print command
            stdin,stdout,stderr = c.exec_command(command)
            print stderr.read(),stdout.read()
        c.close()



print "pub-sub on public networks"
fog = random.choice(fog_device)
vm_name = deployment_output[fog]["host_vm_name"]
host = container_vm[vm_name]["hostname_ip"]
user = container_vm[vm_name]["user"]
key = container_vm[vm_name]["key_path"]
k = paramiko.RSAKey.from_private_key_file(key)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

c.connect(hostname = host, username = user, pkey = k)

nw_name_list = deployment_output[fog]["public_networks"].keys()
fog_ip = deployment_output[fog]["public_networks"][nw_name_list[0]]

commands = [
    "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(fog,path,pub_sub_data),
    "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(fog,path,pub_sub),
    "sudo docker cp -a {0} {1}:{2}".format(pub_sub,fog,path),
    "sudo docker exec -i {0} python {1}/{2}/mqtt.py {3}".format(fog,path,pub_sub,fog_ip),
    "sudo docker exec -i {0} systemctl start mosquitto".format(fog)
]
for command in commands:
    print command
    stdin , stdout, stderr = c.exec_command(command)
    print stderr.read(),stdout.read()
c.close()





for n in public_networks_dict:
    #fog = random.choice(fog_device)
    #nw_name_list = deployment_output[fog]["public_networks"].keys()
    #fog_ip = deployment_output[fog]["public_networks"][nw_name_list[0]]
    #print fog_ip
    device_list = public_networks_dict[n]["devices"]
    print device_list

    sensor_link_list = []
    for device in device_list:
        sensors_list = deployment_output[device]["sensors"]
        for sensor in sensors_list:
            for link in sensor["links"]:
                sensor_link_list.append(link)

    print sensor_link_list

    #pf = open("publisher_list.txt", "w");

    while len(device_list) >= 2:
        devices = random.sample(device_list,2)
        print "Devices --> ",devices
        topic = ''.join(random.choice(string.ascii_lowercase) for _ in range(32))
        print "Topic --> " + topic
        sensor_link = random.choice(sensor_link_list)
        print "sensor_link --> " + sensor_link
        print
        cmd = [
            "python {0}/{1}/subscribe.py {2} {3}".format(path,pub_sub,topic,fog_ip),
            "python {0}/{1}/publish.py {2} {3} {4} {5}".format(path,pub_sub,topic,fog_ip,sensor_link,num_msgs)
        ]

        #print command
        i=0
        for device in devices:
            vm_name = deployment_output[device]["host_vm_name"]
            host = container_vm[vm_name]["hostname_ip"]
            user = container_vm[vm_name]["user"]
            key = container_vm[vm_name]["key_path"]
            k = paramiko.RSAKey.from_private_key_file(key)
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(hostname = host, username = user, pkey = k)

            commands = [
                "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(device,path,pub_sub_data),
                "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(device,path,pub_sub),
                "sudo docker cp -a {0} {1}:{2}".format(pub_sub,device,path,pub_sub),
                "sudo docker exec -id {0} {1}".format(device,cmd[i])
            ]
            if i == 1:
                pf.write(device + " " + topic + "\n")

            for command in commands:
                print command
                stdin,stdout,stderr = c.exec_command(command)
                print stderr.read(),stdout.read()
            c.close()

            i=1
            #time.sleep(2)

        for device in devices:
            device_list.remove(device)

        sensor_link_list.remove(sensor_link)

    if len(device_list) == 1:
        device = device_list[0]
        print "Devices --> ",device
        topic = ''.join(random.choice(string.ascii_lowercase) for _ in range(32))
        print "Topic --> " + topic
        sensor_link = random.choice(sensor_link_list)
        print "sensor_link --> " + sensor_link
        print


        vm_name = deployment_output[device]["host_vm_name"]
        host = container_vm[vm_name]["hostname_ip"]
        user = container_vm[vm_name]["user"]
        key = container_vm[vm_name]["key_path"]
        k = paramiko.RSAKey.from_private_key_file(key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname = host, username = user, pkey = k)

        commands = [
            "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(device,path,pub_sub_data),
            "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(device,path,pub_sub),
            "sudo docker cp -a {0} {1}:{2}".format(pub_sub,device,path,pub_sub),
            "sudo docker exec -id {0} python {1}/{2}/subscribe.py {3} {4}".format(device,path,pub_sub,topic,fog_ip),
            "sudo docker exec -id {0} python {1}/{2}/publish.py {3} {4} {5} {6}".format(device,path,pub_sub,topic,fog_ip,sensor_link,num_msgs)
        ]
        pf.write(device + " " + topic + "\n")

        for command in commands:
            print command
            stdin,stdout,stderr = c.exec_command(command)
            print stderr.read(),stdout.read()
        c.close()




pf.close()

print datetime.now() - startTime

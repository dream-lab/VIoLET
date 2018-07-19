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


log_file = open("pub_sub.log","w")

infra_config = json.load(open("../../config/infra_config.json"))
deployment_output = json.load(open("../../dump/infra/deployment_output.json"))
all_device_list = deployment_output.keys()
private_networks_dict = infra_config["private_networks"]
public_networks_dict = infra_config["public_networks"]
vm_config = json.load(open("../../config/vm_config.json"))


fog_device = []
log_file.write("Fog Devices : ")
for d in all_device_list:
    if "Fog" in d:
        fog_device.append(d)
        log_file.write(d + " ")
print fog_device
log_file.write("\n")

container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()

pub_sub = "scripts"
pub_sub_data = "data"
path = "violet/sanity/pub_sub"

log_file.write("path = " + path + "\n")
log_file.write("pub_sub = " + pub_sub + "\n")
log_file.write("pub_sub_data = " + pub_sub_data + "\n")

num_msgs = "180"
try:
    num_msgs = sys.argv[1]
except IndexError:
    print "Default number of messages is set"

print "Number of Messages = {0}".format(num_msgs)
log_file.write("number of messages = " + num_msgs + "\n")

public_port = 1884
private_port = 1885

log_file.write("public_port = " + str(public_port) + "\n")
log_file.write("private_port = " + str(private_port) + "\n")

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

log_file.write("\n\n\n************************PUB - SUB*****************************\n\n\n")
for i in range(len(container_vm_names)):
    key_path = container_vm[container_vm_names[i]]["key_path"]
    user = container_vm[container_vm_names[i]]["user"]
    host = container_vm[container_vm_names[i]]["hostname_ip"]
    os.system("scp -r -i {0} {1} {2}@{3}:/home/{2}".format(key_path, pub_sub, user, host))



print "Binding Broker address to Mosquitto....."
log_file.write("\n\nBinding Broker address to Mosquitto.....\n\n")

network = "private"
log_file.write("\nNetwork = " + network + "\n")

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
        "sudo docker exec -i {0} python {1}/{2}/mqtt.py {3} {4}".format(fog,path,pub_sub,fog_ip,network),
        "sudo docker exec -i {0} mosquitto -c /etc/mosquitto/mosquitto-{2}.conf -p {1} -d".format(fog,private_port,network)
    ]
    for command in commands:
        #print command
        stdin , stdout, stderr = c.exec_command(command)
        log_file.write("\n" + command + "\n")
        log_file.write("\n" + stdout.read() + "\n")
        log_file.write("\n" + stderr.read() + "\n")
        #print stderr.read(),stdout.read()
    c.close()


pub_sub_broker_list = []
for n in private_networks_dict:
    broker = private_networks_dict[n]["gateway"]
    nw_name_list = deployment_output[broker]["private_networks"].keys()
    broker_ip = deployment_output[broker]["private_networks"][nw_name_list[0]]

    device_list = private_networks_dict[n]["devices"]
    sensor_link_list = []
    for device in device_list:
        sensors_list = deployment_output[device]["sensors"]
        for sensor in sensors_list:
            for link in sensor["links"]:
                sensor_link_list.append(link)

    #print sensor_link_list
    pub = ""
    sub = ""
    while len(device_list) >= 2:
        devices = random.sample(device_list,2)
	sub = devices[0]
	pub = devices[1]
	print "Publisher --> ",pub
	print "Subscriber --> ",sub
        log_file.write("\nPublisher --> " + pub)
	log_file.write("\nSubscriber --> " + sub)
        topic = ''.join(random.choice(string.ascii_lowercase) for _ in range(32))
        print "Topic --> " + topic
        log_file.write("\nTopic -- >" + topic)
        sensor_link = random.choice(sensor_link_list)
        print "sensor_link --> " + sensor_link
        log_file.write("\nsensor_link --> " + sensor_link)
        print
	pub_sub_broker_list.append(pub+" "+sub+" "+broker+" "+topic+" "+network+" "+sensor_link)
        
	cmd = [
            "python {0}/{1}/subscribe.py {2} {3} {4}".format(path,pub_sub,topic,broker_ip,network),
            "python {0}/{1}/publish.py {2} {3} {4} {5} {6}".format(path,pub_sub,topic,broker_ip,sensor_link,num_msgs,network)
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

            for command in commands:
                #print command
                stdin,stdout,stderr = c.exec_command(command)
                log_file.write("\n\n" + command + "\n\n")
                log_file.write("\n" + stdout.read() + "\n")
                log_file.write("\n" + stderr.read() + "\n")
                #print stderr.read(),stdout.read()
            c.close()

            i=1

        for device in devices:
            device_list.remove(device)

        sensor_link_list.remove(sensor_link)

    if len(device_list) == 1:
        device = device_list[0]
	pub = device
	sub = device
        print "Publisher --> ",pub
	print "Subscriber --> ",sub
        log_file.write("\nPublisher --> " + pub)
	log_file.write("\nSubscriber --> "+ sub)
        topic = ''.join(random.choice(string.ascii_lowercase) for _ in range(32))
        print "Topic --> " + topic
        log_file.write("\nTopic --> " + topic)
        sensor_link = random.choice(sensor_link_list)
        print "sensor_link --> " + sensor_link
        log_file.write("\nsensor_link --> " + sensor_link)
        print
	pub_sub_broker_list.append(pub+" "+sub+" "+broker+" "+topic+" "+network+" "+sensor_link)

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
            "sudo docker exec -id {0} python {1}/{2}/subscribe.py {3} {4} {5}".format(device,path,pub_sub,topic,broker_ip,network),
            "sudo docker exec -id {0} python {1}/{2}/publish.py {3} {4} {5} {6} {7}".format(device,path,pub_sub,topic,broker_ip,sensor_link,num_msgs,network)
        ]


        for command in commands:
            #print command
            stdin,stdout,stderr = c.exec_command(command)
            log_file.write("\n\n" + command + "\n\n")
            #print stderr.read(),stdout.read()
            log_file.write(stdout.read() + "\n")
            log_file.write(stderr.read() + "\n")
        c.close()



print "pub-sub on public networks"
log_file.write("pub-sub on public networks")
for fog in fog_device:
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

    network = "public"

    commands = [
        "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(fog,path,pub_sub_data),
        "sudo docker exec -i {0} bash -c 'mkdir -p {1}/{2}'".format(fog,path,pub_sub),
        "sudo docker cp -a {0} {1}:{2}".format(pub_sub,fog,path),
        "sudo docker exec -i {0} python {1}/{2}/mqtt.py {3} {4}".format(fog,path,pub_sub,fog_ip,network),
        "sudo docker exec -i {0} mosquitto -c /etc/mosquitto/mosquitto-{2}.conf -p {1} -d".format(fog,public_port,network)
    ]

    for command in commands:
        #print command
        stdin , stdout, stderr = c.exec_command(command)
        log_file.write("\n\n" + command + "\n\n")
        log_file.write(stdout.read() + "\n")
        log_file.write(stderr.read() + "\n")
        #print stderr.read(),stdout.read()

    c.close()



for n in public_networks_dict:
    broker = public_networks_dict[n]["gateway"]
    nw_name_list = deployment_output[broker]["public_networks"].keys()
    broker_ip = deployment_output[broker]["public_networks"][nw_name_list[0]]
    device_list = public_networks_dict[n]["devices"]

    sensor_link_list = []

    for device in device_list:
        sensors_list = deployment_output[device]["sensors"]
        for sensor in sensors_list:
            for link in sensor["links"]:
                sensor_link_list.append(link)


    while len(device_list) >= 2:
        devices = random.sample(device_list,2)
	sub = devices[0]
	pub = devices[1]
        print "Publisher --> ",pub
	print "Subscriber --> ",sub
        log_file.write("\nPublisher --> " + pub)
	log_file.write("\nSubscriber --> " + sub)
        topic = ''.join(random.choice(string.ascii_lowercase) for _ in range(32))
        print "Topic --> " + topic
        log_file.write("\nTopic --> " + topic)
        sensor_link = random.choice(sensor_link_list)
        print "sensor_link --> " + sensor_link
        log_file.write("\nsensor_link --> " + sensor_link)
        print
	pub_sub_broker_list.append(pub+" "+sub+" "+broker+" "+topic+" "+network+" "+sensor_link)

        cmd = [
            "python {0}/{1}/subscribe.py {2} {3} {4}".format(path,pub_sub,topic,broker_ip,network),
            "python {0}/{1}/publish.py {2} {3} {4} {5} {6}".format(path,pub_sub,topic,broker_ip,sensor_link,num_msgs,network)
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

            for command in commands:
               # print command
                stdin,stdout,stderr = c.exec_command(command)
                log_file.write("\n\n" + command + "\n\n")
                log_file.write(stdout.read() + "\n")
                log_file.write(stderr.read())
                #print stderr.read(),stdout.read()
            c.close()

            i=1
            #time.sleep(2)

        for device in devices:
            device_list.remove(device)

        sensor_link_list.remove(sensor_link)

    if len(device_list) == 1:
        device = device_list[0]
	pub = device
	sub = device
        print "Publisher --> ",pub
	print "Subscriber --> ",sub
        log_file.write("\nPublisher --> " + pub)
	log_file.write("\nSubscriber --> "+ sub)
        topic = ''.join(random.choice(string.ascii_lowercase) for _ in range(32))
        print "Topic --> " + topic
        log_file.write("\nTopic --> " + topic)
        sensor_link = random.choice(sensor_link_list)
        print "sensor_link --> " + sensor_link
        log_file.write("\nsensor_link --> " + sensor_link)
        print
	pub_sub_broker_list.append(pub+" "+sub+" "+broker+" "+topic+" "+network+" "+sensor_link)

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
            "sudo docker exec -id {0} python {1}/{2}/subscribe.py {3} {4} {5}".format(device,path,pub_sub,topic,broker_ip,network),
            "sudo docker exec -id {0} python {1}/{2}/publish.py {3} {4} {5} {6} {7}".format(device,path,pub_sub,topic,broker_ip,sensor_link,num_msgs,network)
        ]

        for command in commands:
            #print command
            stdin,stdout,stderr = c.exec_command(command)
            log_file.write("\n\n" + command + "\n\n")
            log_file.write(stdout.read() + "\n")
            log_file.write(stderr.read() + "\n")
            #print stderr.read(),stdout.read()
        c.close()

total_time = datetime.now() - startTime
print total_time
log_file.write(str(total_time))
print "Please wait for {} seconds to finish".format(num_msgs)
log_file.close()




f = open("pub_sub_broker.txt","w")
for p in pub_sub_broker_list:
	f.write(p+"\n")
f.close()


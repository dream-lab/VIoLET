import os
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
devices = json.load(open('../../dump/infra/infra_devices.json'))
private_networks_dict = json.load(open('../../dump/infra/infra_pvt.json'))
#public_networks_dict = json.load(open('../../dump/infra/infra_pub.json'))
device_vm = json.load(open('../../dump/infra/infra_device_vm.json'))
device_ip = json.load(open('../../dump/infra/infra_device_ip.json'))
#cloud_device = json.load(open('dump/infra-cloud-devices'))
fog_device = json.load(open('../../dump/infra/infra_fog_devices.json'))
#ip_device = {v: k for k, v in device_ip.iteritems()}
edge_device = json.load(open('../../dump/infra/infra_edge_devices.json'))
infra_devices_with_sensors = json.load(open('../../dump/infra/infra_devices_with_sensors.json'))
vm_config = json.load(open("../../config/vm_config.json"))
fog_sensor_link = json.load(open("../../dump/infra/infra_fog_sensor_link.json"))

container_vm = vm_config["container_host_VM"]
container_vm_names = container_vm.keys()


#pub_sub_tar = "scripts.tar.gz"
pub_sub = "scripts"


#Create AWS connection
#k = paramiko.RSAKey.from_private_key_file("/home/centos/CIBO-CentOS.pem")
#c = paramiko.SSHClient()
#c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#user="centos"






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
    host = container_vm[container_vm_names[i]]["public_DNS"]
    os.system("scp -r -i {0} {1} {2}@{3}:/home/{2}".format(key_path, pub_sub, user, host))



print "Binding Broker address to Mosquitto....."

for fog in fog_device:
    vm_name = device_vm[fog]
    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect(hostname = host, username = user, pkey = k)

    ip = device_ip[fog]
    #os.system("scp -r -i {0} {1} {2}@{3}:/home/{2}".format(key, pub_sub, user, host))
    command = "sudo docker cp -a {0} {1}:/".format(pub_sub,fog)
    stdin , stdout, stderr = c.exec_command(command)
    time.sleep(1)
    command =  "sudo docker exec -i {0} python {1}/mqtt.py {2}".format(fog,pub_sub,ip)
    #print command
    stdin , stdout, stderr = c.exec_command(command)
    #print stderr.read()
    time.sleep(2)
    print "starting broker at {0} on {1}".format(ip,fog)
    command = "sudo docker exec -i {0} systemctl start mosquitto".format(fog)
    stdin , stdout, stderr = c.exec_command(command)
    #print stderr.read(),stdout.read()
    c.close()




for n in private_networks_dict:
    #total = len(private_networks_dict[n]["conn_dev"])
    #print "number of edge devices"
    #print total
    #cnt = 0
    fog = private_networks_dict[n]["gw"]
    ip = device_ip[fog]
    sensor_link_list = fog_sensor_link[ip]
    print ip

    device_list=private_networks_dict[n]["conn_dev"]

    while len(device_list) >= 2:
        devices = random.sample(device_list,2)
        #print devices
        topic = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        #print topic
        sensor_link = random.sample(sensor_link_list,1)[0]
        cmd = [
            "python {0}/subscribe.py {1} {2}".format(pub_sub,topic,ip),
            "python {0}/publish.py {1} {2} {3}".format(pub_sub,topic,ip,sensor_link)
        ]

        #print command
        i=0
        for device in devices:
            print device
            vm_name = device_vm[device]
            host = container_vm[vm_name]["public_DNS"]
            user = container_vm[vm_name]["user"]
            key = container_vm[vm_name]["key_path"]
            k = paramiko.RSAKey.from_private_key_file(key)
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(hostname = host, username = user, pkey = k)

            command = "sudo docker cp -a {0} {1}:/".format(pub_sub,device)
            stdin,stdout,stderr = c.exec_command(command)
            time.sleep(1)
            command = "sudo docker exec -id {0} {1}".format(device,cmd[i])
            #print command
            stdin,stdout,stderr = c.exec_command(command)
            c.close()

            i+=1

        for device in devices:
            device_list.remove(device)

        sensor_link_list.remove(sensor_link)


print datetime.now() - startTime

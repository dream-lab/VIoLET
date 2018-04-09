import os
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
hosts = json.load(open('../../dump/infra-hosts'))
devices = json.load(open('../../dump/infra/infra_devices.json'))
private_networks_dict = json.load(open('../../dump/infra/infra_pvt.json'))
public_networks_dict = json.load(open('../../dump/infra/infra_pub.json'))
device_vm = json.load(open('../../dump/infra/infra_device_vm.json'))
device_ip = json.load(open('../../dump/infra/infra_device_ip.json'))
#cloud_device = json.load(open('dump/infra-cloud-devices'))
fog_device = json.load(open('../../dump/infra/infra_fog_devices.json'))
ip_device = {v: k for k, v in device_ip.iteritems()}
edge_device = json.load(open('../../dump/infra/infra_edge_devices.json'))
infra_devices_with_sensors = json.load(open('../../dump/infra/infra_devices_with_sensors.json'))
vm_config = json.load(open("../../config/vm_config.json"))


container_vm = vm_config["container_host_VM"]
container_vm_names = container_vm.keys()




path = "/home/centos/"
pub_sub_tar = "scripts.tar.gz"
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
    os.system("scp -r -i {0} {1} {2}@{3}:/home/{2}".format(key, pub_sub, user, host))
    #command = "sudo docker exec -i {0} echo \"bind_address {1}\" > /etc/mosquitto/mosquitto.conf".format(fog,ip)
    #command = "tar -zcvf {0} {1}".format(pub_sub_tar,pub_sub)
    #stdin , stdout , stderr = c.exec_command(command)
    time.sleep(2)
    command = "sudo docker cp -a {0} {1}:".format(path + pub_sub,fog)
    stdin , stdout, stderr = c.exec_command(command)
    time.sleep(2)
    #command = "sudo docker exec -i {0} tar -zxvf {1}".format(fog, pub_sub_tar)
    #print command
    #stdin , stdout, stderr = c.exec_command(command)
    #print stderr.read(),stdout.read()
    #time.sleep(2)
    command =  "sudo docker exec -i {0} python mqtt.py {1}".format(fog,ip)
    #print command
    stdin , stdout, stderr = c.exec_command(command)
    print stderr.read()
    time.sleep(2)
    print "starting broker at {0} on {1}".format(ip,fog)
    command = "sudo docker exec -i {0} systemctl start mosquitto".format(fog)
    stdin , stdout, stderr = c.exec_command(command)
    print stderr.read(),stdout.read()
    c.close()




for n in private_networks_dict:
    #print n
    total = len(private_networks_dict[n]["conn_dev"])
    print "number of edge devices"
    print total
    cnt = 0
    fog = private_networks_dict[n]["gw"]
    ip = device_ip[fog]
    print ip
    #f=open("subscriber-list","w")
    #t=0
    for device in private_networks_dict[n]["conn_dev"]:
        vm_name = device_vm[device]
        host = container_vm[vm_name]["public_DNS"]
        user = container_vm[vm_name]["user"]
        key = container_vm[vm_name]["key_path"]
        k = paramiko.RSAKey.from_private_key_file(key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname = host, username = user, pkey = k)
        #ip = device_ip[device]
        #c.connect(hostname = vm, username = user, pkey = k)
        os.system("scp -r -i {0} {1} {2}@{3}:/home/{2}".format(key, pub_sub, user, host))
        time.sleep(2)
        #command = "tar -zcvf {0} {1}".format(pub_sub_tar,pub_sub)
        #stdin , stdout , stderr = c.exec_command(command)
        #print "Copying datagen tar devices"
        command = "sudo docker cp -a {0} {1}:".format(path + pub_sub,device)
        stdin , stdout, stderr = c.exec_command(command)
        time.sleep(2)
        #print "Starting untar of datagen"
        #command = "sudo docker exec -i {0} tar -zxvf {1}".format(device, pub_sub_tar)
        #print command
        #stdin , stdout, stderr = c.exec_command(command)
        #time.sleep(2)
        #print stdout.read()
        #time.sleep(2)

        topic = infra_devices_with_sensors["Edge-1.1"]
        total = len(topic)
        #pub_topic = topic
        if (cnt%2) == 1:
            print "starting publisher on {0}".format(device)
            command = "sudo docker exec -d {0} nohup python publish.py {1} {2}".format(device,topic[int(cnt/2)%total],ip)
            print command
            stdin,stdout,stderr=c.exec_command(command)
            print stderr.read(),stdout.read()
            cnt=cnt+1
        else:
            print "starting subscriber on {0}".format(device)
            command = "sudo docker exec -d {0} nohup python subscribe.py {1} {2} ".format(device,topic[int(cnt/2)%total],ip)
            print command
            stdin,stdout,stderr=c.exec_command(command)
            print stderr.read(),stdout.read()
            cnt=cnt+1
        c.close()


print datetime.now() - startTime

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
hosts = json.load(open('dump/infra-hosts'))
devices = json.load(open('dump/infra-devices'))
private_networks_dict = json.load(open('dump/infra-pvt'))
public_networks_dict = json.load(open('dump/infra-pub'))
device_vm = json.load(open('dump/infra-device-vm'))
device_ip = json.load(open('dump/infra-device-ip'))
#cloud_device = json.load(open('dump/infra-cloud-devices'))
fog_device = json.load(open('dump/infra-fog-devices'))
ip_device = {v: k for k, v in device_ip.iteritems()}
edge_device = json.load(open('dump/infra-edge-devices'))
data_tar = "datagen.tar.gz"

'''print hosts
print
print devices
print
print private_networks_dict
print
print public_networks_dict
print
print device_vm
print
print device_ip
print
print ip_device'''


#Create AWS connection
k = paramiko.RSAKey.from_private_key_file("/home/centos/CIBO-CentOS.pem")
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
user="centos"


print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "               Data Generation                 "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print


print "Binding Broker address to Mosquitto....."
for fog in fog_device:
    vm = device_vm[fog]
    ip = device_ip[fog]
    c.connect(hostname = vm, username = user, pkey = k)
    #command = "sudo docker exec -i {0} echo \"bind_address {1}\" > /etc/mosquitto/mosquitto.conf".format(fog,ip)
    time.sleep(2)
    command = "sudo docker cp {0} {1}:/".format(data_tar,fog)
    stdin , stdout, stderr = c.exec_command(command)
    time.sleep(2)
    command = "sudo docker exec -i {0} tar -zxvf {1}".format(fog, data_tar)
    print command
    stdin , stdout, stderr = c.exec_command(command)
    print stderr.read(),stdout.read()
    time.sleep(2)
    command =  "sudo docker exec -i {0} python datagen/mqtt.py {1}".format(fog,ip)
    print command
    stdin , stdout, stderr = c.exec_command(command)
    print stderr.read()
    #command = "sudo docker exec -i {0} cat /etc/mosquitto/mosquitto.conf".format(fog)
    #stdin , stdout, stderr = c.exec_command(command)
    #print stderr.read(), stdout.read()
    time.sleep(2)
    print "starting broker at {0} on {1}".format(ip,fog)
    command = "sudo docker exec -i {0} systemctl start mosquitto".format(fog)
    stdin , stdout, stderr = c.exec_command(command)
    print stderr.read(),stdout.read()
    c.close()

'''
print "Copying data-gen.tar to devices....."
for device in edge_device:
    vm = device_vm[device]
    ip = device_ip[device]
    c.connect(hostname = vm, username = user, pkey = k)
    time.sleep(2)
    command = "sudo docker cp {0} {1}:/".format(data_tar,device)
    stdin , stdout, stderr = c.exec_command(command)
    time.sleep(2)
    command = "sudo docker exec -i {0} tar -zxvf {1}".format(device, data_tar)
    print command
    stdin , stdout, stderr = c.exec_command(command)
    time.sleep(2)
    print stdout.read()
    print "Starting parser.py in {0}".format(device)
    command = "sudo docker exec -i {0} python datagen/parser.py".format(device)
    print command
    stdin , stdout, stderr = c.exec_command(command)
    print stderr.read(),stdout.read()

    print "Starting app.py in {0}".format(device)
    command = "sudo docker exec -i {0} python datagen/app.py &".format(device)
    stdin , stdout, stderr = c.exec_command(command)
    print command
    print stderr.read()
    c.close()
'''
topics=[ 'Edge-1.1_gyroscope_1',
        'Edge-1.1_gyroscope_2',
        'Edge-1.1_gyroscope_3',
        'Edge-1.1_accelerometer_4',
        'Edge-1.1_accelerometer_5',
        'Edge-1.2_gyroscope_1',
        'Edge-1.2_gyroscope_2',
        'Edge-1.2_gyroscope_3',
        'Edge-1.2_accelerometer_4',
        'Edge-1.2_accelerometer_5',
        'Edge-2.1_gyroscope_1',
        'Edge-2.1_gyroscope_2',
        'Edge-2.1_gyroscope_3',
        'Edge-2.1_accelerometer_4',
        'Edge-2.1_accelerometer_5',
        'Edge-1.1_gyroscope_1',
        'Edge-1.1_gyroscope_2',
        'Edge-1.1_gyroscope_3',
        'Edge-1.1_accelerometer_4',
        'Edge-1.1_accelerometer_5']


#f=open("subscriber-list","w")

for n in private_networks_dict:
    print n
    cnt = len(private_networks_dict[n]["conn_dev"])
    print "number of edge devices"
    print cnt
    fog = private_networks_dict[n]["gw"]
    ip = device_ip[fog]
    print ip
    #f=open("subscriber-list","w")
    t=0
    for device in private_networks_dict[n]["conn_dev"]:
        vm = device_vm[device]
        #ip = device_ip[device]
        c.connect(hostname = vm, username = user, pkey = k)
        time.sleep(2)
        print "Copying datagen tar devices"
        command = "sudo docker cp {0} {1}:/".format(data_tar,device)
        stdin , stdout, stderr = c.exec_command(command)
        time.sleep(2)
        print "Starting untar of datagen"
        command = "sudo docker exec -i {0} tar -zxvf {1}".format(device, data_tar)
        #print command
        stdin , stdout, stderr = c.exec_command(command)
        time.sleep(2)
        print stdout.read()
        print "Starting parser.py in {0}".format(device)
        command = "sudo docker exec -i {0} python datagen/parser.py".format(device)
        #print command
        stdin , stdout, stderr = c.exec_command(command)
        print stderr.read(),stdout.read()
        print "Starting app.py in {0}".format(device)
        command = "sudo docker exec -i {0} nohup python datagen/app.py &".format(device)
        stdin , stdout, stderr = c.exec_command(command)
        #print command
        print stderr.read(),stdout.read()


        #f=open("subscriber-list","a+"  )

        if (cnt%2) == 1:
            print "starting publisher on {0}".format(device)
            #f.write("{0}\n".format(device))
            print ip
            cnt=cnt-1
            print cnt
            command = "sudo docker exec -d {0} nohup python datagen/publish.py {1} {2}".format(device,topics[int(t%20)],ip)
            print command
            t=t+1
            stdin,stdout,stderr=c.exec_command(command)
            print stderr.read(),stdout.read()
        else:
            print "starting subscriber on {0}".format(device)
            print ip
            cnt=cnt-1
            print cnt
            command = "sudo docker exec -d {0} nohup python datagen/subscribe.py {1} {2} ".format(device,topics[int(t%20)],ip)
            print command
            #t=t+1
            stdin,stdout,stderr=c.exec_command(command)
            print stderr.read(),stdout.read()
        #f.close()

        c.close()
#f.close()

print datetime.now() - startTime

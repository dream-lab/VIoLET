import json
import time
import sys
import os
import math
import random
import paramiko


coremark_exe = "violet/coremark_exe"
device_down_set = set()

'''
def read_cm(device):
	vm_name = deployment_output[device]["host_vm_name"]
        host = container_vm[vm_name]["hostname_ip"]
        user = container_vm[vm_name]["user"]
        key = container_vm[vm_name]["key_path"]
        k = paramiko.RSAKey.from_private_key_file(key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname = host, username = user, pkey = k)

	print "\n\nCollecting numbers in {0}".format(device)
        command = "sudo docker exec -i {0} cat results-coremark | grep \"CoreMark 1.0\" | awk '{{print $4}}'".format(device)
        stdin , stdout, stderr = c.exec_command(command)
        #print stderr.read()

        observed_coremark = stdout.read()

        command = "sudo docker exec -i {0} cat results-coremark | grep start_time | awk -F '=' '{{print $2}}'".format(device)
        stdin , stdout2, stderr = c.exec_command(command)
        #print stderr.read()

        start_time = stdout2.read()
        start_time = start_time.split("\n")

        command = "sudo docker exec -i {0} cat results-coremark | grep end_time | awk -F '=' '{{print $2}}'".format(device)
        stdin , stdout3, stderr = c.exec_command(command)
        #print stderr.read()

        end_time = stdout3.read()
        end_time = end_time.split("\n")

	observed_coremark = observed_coremark.split("\n")
        observed_coremark.pop()
	coremark = []
        for i in observed_coremark:
            coremark.append(float(i))
	

	d_type = infra_config["devices"][device]["device_type"]

	coremark_str = []
        start_str = []
        end_str = []

        for c_str in coremark:
            coremark_str.append(str(c_str))
        for s_str in start_time:
            start_str.append(str(s_str))
        for e_str in end_time:
            end_str.append(str(e_str))

	f = open("../../dump/resource_dynamism/mttf/device_cm/{}".format(device),"a+")

	print(d_type,coremark)
	for i in range(len(coremark)):
            f.write(device+"\t"+d_type+"\t"+vm_name+"\t"+str(coremark[i])+"\t"+str(start_time[i])+"\t"+str(end_time[i])+"\n")

	f.close()
	c.close()

'''


def device_down(devices,devices_data,devices_down):
    print 
    print "Active Devices - {}".format(len(devices))
    print 
    for d in devices:
        r = random.uniform(0.0, 1.0)
        #print "Device - {0} r - {1} p - {2}".format(d,r,probability)
	d_type = devices_data[d]["d_type"]
	mttf = devices_data[d]["mttf"]
	mttf_prob = devices_data[d]["mttf_prob"]

	start = time.time()
        
	if r <= mttf_prob:
	    print "Device down - {0} r - {1} p - {2}".format(d,r,mttf_prob)
            vm_name = deployment_output[d]["host_vm_name"]
            host = container_vm[vm_name]["hostname_ip"]
            user = container_vm[vm_name]["user"]
            key = container_vm[vm_name]["key_path"]
            k = paramiko.RSAKey.from_private_key_file(key)
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(hostname = host, username = user, pkey = k)

	    #read_cm(d)
	    #print
            command="sudo docker stop {}".format(d)
	    
	    start = time.time()
            stdin, stdout, stderr = c.exec_command(command,timeout=60)
	    #print stderr.read()
	    end = time.time()
	    mttf_dynamism.write("{0},{1},{2},{3},{4},{5},{6}\n".format(d,d_type,start,end,"inactive",r,mttf_prob))
	    c.close()
            devices.remove(d)
	    devices_down.append(d)
	    device_down_set.add(d)
	else:
	    end = time.time()
	    mttf_dynamism.write("{0},{1},{2},{3},{4},{5},{6}\n".format(d,d_type,start,end,"active",r,mttf_prob))

    for d in devices_down:
	r = random.uniform(0.0, 1.0)
        #print "Device - {0} r - {1} p - {2}".format(d,r,probability)
        d_type = devices_data[d]["d_type"]
        mttr = devices_data[d]["mttr"]
        mttr_prob = devices_data[d]["mttr_prob"]

        start = time.time()
        
        if r <= mttr_prob:
            print "Device up - {0} r - {1} p - {2}".format(d,r,mttr_prob)
            vm_name = deployment_output[d]["host_vm_name"]
            host = container_vm[vm_name]["hostname_ip"]
            user = container_vm[vm_name]["user"]
            key = container_vm[vm_name]["key_path"]
            k = paramiko.RSAKey.from_private_key_file(key)
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(hostname = host, username = user, pkey = k)
	    '''
	    device_type = infra_config["devices"][d]["device_type"]

            if (device_type == "SI"):
            	path = "{0}/si/coremark.exe".format(coremark_exe)
            else:
            	path = "{0}/pi/coremark.exe".format(coremark_exe)	    

            '''
	    command = "sudo docker start {}".format(d)
            start = time.time()
            stdin, stdout, stderr = c.exec_command(command,timeout=60)
	    #print stderr.read()
            end = time.time()
	    # starting coremark again for remaining time
	    #cm_run_time = abs(int(end_time - end))
	    #command = "sudo docker exec -d {0} python {1}/c_coremark.py {2} {3}".format(d,coremark_exe,path,cm_run_time)
	    #print("starting coremark\n{}".format(command))
	    #stdin, stdout, stderr = c.exec_command(command,timeout=60)
	    #print stderr.read()
            c.close()
            mttf_dynamism.write("{0},{1},{2},{3},{4},{5},{6}\n".format(d,d_type,start,end,"active",r,mttr_prob))
            devices.append(d)
	    devices_down.remove(d)
        else:
            end = time.time()
            mttf_dynamism.write("{0},{1},{2},{3},{4},{5},{6}\n".format(d,d_type,start,end,"inactive",r,mttr_prob))
	



infra_config = json.load(open("../../config/infra_config.json"))
vm_config = json.load(open("../../config/vm_config.json"))
device_types = json.load(open("../../config/device_types.json"))
vm_types = json.load(open("../../config/vm_types.json"))
deployment_json = json.load(open("../../config/deployment.json"))
deployment_output = json.load(open("../../dump/infra/deployment_output.json"))
all_devices_list = infra_config["devices"].keys()
container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()

devices = infra_config["devices"]
dev_names = devices.keys()
devices_down = []

control_interval = float(deployment_json["control_interval_secs"])
dynamism_duration = int(sys.argv[1]) #float(deployment_json["dynamism_duration_secs"])

devices_data = {}

os.system("rm -rf ../../dump/resource_dynamism/mttf/device_cm")

os.system("mkdir -p ../../dump/resource_dynamism/mttf/device_cm")

start_time_epoch = time.time()
actual_start_time_epoch = start_time_epoch
start_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(start_time_epoch))
print "\nStart time =  [{}] \n".format(start_time)
print "List of devices\n"
print devices
print
n = len(devices)

#end_time = start_time_epoch + dynamism_duration
#print "End time - {0}".format(end_time)




for d in devices:
    d_type = devices[d]["device_type"]
    mttf = int(device_types[d_type]["reliability"]["mttf_sec"])
    mttr = int(device_types[d_type]["reliability"]["mttr_sec"])
    mttf_prob = control_interval/mttf
    mttr_prob = control_interval/mttr
    devices_data[d] = {
	"d_type":d_type,
	"mttf":mttf,
	"mttr":mttr,
	"mttf_prob":mttf_prob,
	"mttr_prob":mttr_prob
    }
    #f = open("../../dump/resource_dynamism/mttf/device_cm/{}".format(d),"w")
    #f.write("Coremark\n")
    #f.close()
'''
for d in devices:
    vm_name = deployment_output[d]["host_vm_name"]
    host = container_vm[vm_name]["hostname_ip"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname = host, username = user, pkey = k)
    device_type = infra_config["devices"][d]["device_type"]
    if (device_type == "SI"):
	path = "{0}/si/coremark.exe".format(coremark_exe)
    else:
        path = "{0}/pi/coremark.exe".format(coremark_exe)

    # starting coremark again for remaining time
    cm_run_time = int(dynamism_duration)
    print "Starting coremark in {0}".format(d)
    command = "sudo docker exec -d {0} python {1}/c_coremark.py {2} {3}".format(d,coremark_exe,path,cm_run_time)
    stdin, stdout, stderr = c.exec_command(command,timeout=60)
    print command,stderr.read()
    c.close()
'''

#os.system("mkdir -p ../../dump/resource_dynamism/mttf_mttr/device_cm")

mttf_dynamism = open("../../dump/resource_dynamism/mttf/mttf_dynamism_raw.txt","w")
#mttr_dynamism = open("../../dump/resource_dynamism/mttf_mttr/mttr_dynamism_raw.txt","w")

#print
#print "waiting for coremark to execute for atleast once (60 seconds)"
#print
#time.sleep(60)

end_time = time.time() + int(dynamism_duration)
#print "End time - {0}".format(end_time)


while(True):
    current_time_epoch = time.time()
    if (current_time_epoch > end_time):
	break
    diff = int (current_time_epoch - start_time_epoch)
    if(diff >= control_interval):
	print "\n\n***control_interval***"
    	current_time_epoch = time.time()
    	current_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(current_time_epoch))
    	print "start_time = {0} \tcurrent_time = {1} \ttime elapsed = {2} \tmttf = {3}".format(start_time,current_time,int(current_time_epoch - actual_start_time_epoch), mttf)
        start_time_epoch = time.time()
        val = device_down(dev_names,devices_data,devices_down)
        if (val == -1):
            break

mttf_dynamism.close()
#mttr_dynamism.close()

print device_down_set

print
print "Bringing down devices up again\n"
for d in devices_down:
    vm_name = deployment_output[d]["host_vm_name"]
    host = container_vm[vm_name]["hostname_ip"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname = host, username = user, pkey = k)

    command = "sudo docker start {}".format(d)
    '''
    print command
    #start = time.time()
    stdin, stdout, stderr = c.exec_command(command,timeout=60)
    #end = time.time()
    device_type = infra_config["devices"][d]["device_type"]
    if (device_type == "SI"):
        path = "{0}/si/coremark.exe".format(coremark_exe)
    else:
        path = "{0}/pi/coremark.exe".format(coremark_exe)

    # starting coremark again for remaining time
    cm_run_time = int(60)
    print "Starting coremark in {0}".format(d)
    command = "sudo docker exec -d {0} python {1}/c_coremark.py {2} {3}".format(d,coremark_exe,path,cm_run_time)
    stdin, stdout, stderr = c.exec_command(command,timeout=60)
    print command,stderr.read()
    '''
    c.close()

print
#print "waiting for coremark to finish (60 seconds)"
print
#time.sleep(60)

devices = infra_config["devices"].keys()
'''
for device in devices:
	read_cm(device)
'''

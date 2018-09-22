import json
import time
import sys
import os
import math
import random
from datetime import datetime
import paramiko

def action_ci(devices,devices_data):
    for d in devices:
        r = random.uniform(0.0, 1.0)
        #print "Device - {0} r - {1} p - {2}".format(d,r,probability)
	d_type = devices_data[d]["d_type"]
	prev_coremark = device_types[d_type]["coremark"]
	coremark = prev_coremark
	probability = devices_data[d]["probability"]
	cpu_var = devices_data[d]["cpu_var"]        #float(device_types[d_type]["reliability"]["cpu_var_max"])
        cpu_var_period = devices_data[d]["cpu_var_period"]  #float(device_types[d_type]["reliability"]["cpu_var_period_sec"])
        coremark_max = devices_data[d]["coremark_max"]      #float(device_types[d_type]["coremark"])
        coremark_min = devices_data[d]["coremark_min"]  
	#print "Device - {0} r - {1} p - {2}".format(d,r,probability)
	start = time.time()
        #Device CM will be updated based on the cpu_var_max
	if r <= probability:
	    #begin = time.time()
            cpu_cm = {}
	    #d_type = devices[d]["device_type"]
	    print "Device - {0} r - {1} p - {2}".format(d,r,probability)
	    # Preprocessing step (1 time)
	    # Getting device details
	    #d_type = devices_data[d]["d_type"]
	    #cpu_var = devices_data[d]["cpu_var"]	#float(device_types[d_type]["reliability"]["cpu_var_max"])
	    #cpu_var_period = devices_data[d]["cpu_var_period"]	#float(device_types[d_type]["reliability"]["cpu_var_period_sec"])
	    #coremark_max = devices_data[d]["coremark_max"]	#float(device_types[d_type]["coremark"])
	    #coremark_min = devices_data[d]["coremark_min"]	#coremark_max * (1 - cpu_var)
	    
	    if d in device_cpus_updated:
		prev_coremark = device_cpus_updated[d]["coremark"]
            #print "Inside *IF*"
            coremark = random.uniform(coremark_min,coremark_max)
            #coremark = (coremark_min + coremark_max) / 2.0
            #coremark = coremark_min
            coremark = math.ceil(coremark)
            vm_name = deployment_output[d]["host_vm_name"]
            vm_type = vm_config["container_VM"][vm_name]["vm_type"]
            vm_coremark = vm_types[vm_type]["coremark"]
            vm_core_count = vm_types[vm_type]["core_count"]
            cpus_updated = float(coremark)/ float(vm_coremark) * float(vm_core_count)
            cpus_updated = float("{0:.2f}".format(cpus_updated))
            cpu_cm["cpus"] = cpus_updated
            cpu_cm["coremark"] = coremark
	    
	    start = time.time()	

            host = container_vm[vm_name]["hostname_ip"]
            user = container_vm[vm_name]["user"]
            key = container_vm[vm_name]["key_path"]
            k = paramiko.RSAKey.from_private_key_file(key)
            c = paramiko.SSHClient()
            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(hostname = host, username = user, pkey = k)

            command = "sudo docker update --cpus={0} {1}".format(cpus_updated,d)
            stdin, stdout, stderr = c.exec_command(command,timeout=5)
            #print stdout.read()
            #print stderr.read()
	    
	    end = time.time()
	    cpu_dynamism.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n".format(d,d_type,start,end,coremark_max,coremark_min,prev_coremark,coremark,"yes",r,probability))
            print "Device {0} updated [cpus = {1}, coremark = {2}]".format(d, cpus_updated, coremark)
            device_cpus_updated [d] = cpu_cm
	else:
	    end = time.time()
	    cpu_dynamism.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n".format(d,d_type,start,end,coremark_max,coremark_min,prev_coremark,coremark,"no",r,probability))

    with open('../../dump/resource_dynamism/cpu_dynamism/device_cpus_updated_{0}.json'.format(d_type),'w') as file:
        file.write(json.dumps(device_cpus_updated))

infra_config = json.load(open("../../config/infra_config.json"))
vm_config = json.load(open("../../config/vm_config.json"))
device_types = json.load(open("../../config/device_types.json"))
vm_types = json.load(open("../../config/vm_types.json"))
deployment_json = json.load(open("../../config/deployment.json"))
deployment_output = json.load(open("../../dump/infra/deployment_output.json"))
all_devices_list = infra_config["devices"].keys()
container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()
device_cpus_updated = {}
#d_type = sys.argv[1]
devices = infra_config["devices"]

control_interval = float(deployment_json["control_interval_secs"])
#probability = float(control_interval)/float(cpu_var_period)
dynamism_duration = float(deployment_json["dynamism_duration_secs"])


print "Starting coremark on all devices:"
os.chdir("../../")
#p = subprocess.Popen([command, argument1,...], cwd=working_directory)
os.system("python sanity_cpu.py 1")
os.chdir("apps/cpu_dynamic")

devices_data = {}

for d in devices:
    d_type = devices[d]["device_type"]
    cpu_var = float(device_types[d_type]["reliability"]["cpu_var_max"])
    cpu_var_period = float(device_types[d_type]["reliability"]["cpu_var_period_sec"])
    coremark_max = float(device_types[d_type]["coremark"])
    coremark_min = coremark_max * (1 - cpu_var)
    probability = float(control_interval)/float(cpu_var_period)
    devices_data[d] = {
	"d_type":d_type,
	"cpu_var":cpu_var,
	"cpu_var_period":cpu_var_period,
	"coremark_max":coremark_max,
	"coremark_min":coremark_min,
	"probability":probability
    }

cpu_dynamism = open("../../dump/resource_dynamism/cpu_dynamism/cpu_dynamism_raw.txt","w")


#for d in all_devices_list:
#    if infra_config["devices"][d]["device_type"] == d_type:
#        devices.append(d)

start_time_epoch = time.time()
start_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(start_time_epoch))
print "start time =  [{0}] \n  cpu_var = {1} \n  cpu_var_period = {2} sec \n  coremark_max = {3}\n  coremark_min ={4}\n  control_interval = {5}\n  probability = {6}\n\n".format(start_time, cpu_var, cpu_var_period, coremark_max, coremark_min, control_interval, probability)
#cpu_dynamism.write("start time =  [{0}] \n  cpu_var = {1} \n  cpu_var_period = {2} sec \n  coremark_max = {3}\n  coremark_min ={4}\n  control_interval = {5}\n  probability = {6}\n\n".format(start_time, cpu_var, cpu_var_period, coremark_max, coremark_min, control_interval, probability))

print "List of devices\n\n {0}".format(devices)
print

end_time = start_time_epoch + dynamism_duration
print "End time - {0}".format(end_time)

cpu_dynamism.write("{0},{1},{2},{3},{4},{5},{6}\n".format("device_id", "device_type","start_time","end_time","max_coremark","min_coremark","previous_coremark","updated_coremark","status","random value","probability"))

while(True):
    current_time_epoch = time.time()
    if (current_time_epoch > end_time):
	break
    diff = int (current_time_epoch - start_time_epoch)
    if(diff >= control_interval):
        print "\n\n**********Action time! [{0}]**********\n".format(time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(current_time_epoch)))
	#cpu_dynamism.write("\n\n**********Action time! [{0}]**********\n".format(time.strftime("%a, %d %b %Y %H:%M:%S %Z",time.localtime(current_time_epoch))))
        start_time_epoch = time.time()
        action_ci(devices,devices_data)

print "Completed."
print "Run Sanity."

cpu_dynamism.close()


print "check if coremarks are still running. If not run python ../../sanity_cpu.py 2"


os.chdir("../../")
os.system("python sanity_cpu.py 2")


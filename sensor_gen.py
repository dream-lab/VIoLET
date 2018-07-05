import os
import paramiko
import random
import time
import json
from datetime import datetime
from threading import Thread

infra_config = json.load(open("config/infra_config.json"))
vm_config = json.load(open("config/vm_config.json"))
sensor_types =  json.load(open("config/sensor_types.json"))
deployment =  json.load(open("config/deployment.json"))
deployment_output = json.load(open("dump/infra/deployment_output.json"))


all_devices_list = deployment_output.keys()
print all_devices_list
container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()


path = "VIoLET"
sensor_path = path + "/sensors"
sensor_bin_path = sensor_path + "/bin"
sensor_data_path = sensor_path + "/data"



print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "             Copy data to other VMs            "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

sensors_data_gen = "sensors_data_gen"

for i in range(len(container_vm_names)):
    key_path = container_vm[container_vm_names[i]]["key_path"]
    user = container_vm[container_vm_names[i]]["user"]
    host = container_vm[container_vm_names[i]]["hostname_ip"]
    os.system("scp -rp -i {0} {1} {2}@{3}:/home/{2}".format(key_path, sensors_data_gen, user, host))



print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "           Create sensors                      "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print


sensor_types_list = sensor_types["sensor_types"]

sensor_types_dict = {}

for sensor in sensor_types_list:
    sensor_id = str(sensor["id"])
    timestamp = str(sensor["timestamp"])
    sample_size = str(sensor["sample_size"])
    dist_rate = str(sensor["dist_rate"])
    dist_value = str(sensor["dist_value"])

    if str(sensor["dist_rate"]) == "normal" :
        mean = sensor["rate_params"]["mean"]
        variance = sensor["rate_params"]["variance"]
        min_value = sensor["rate_params"]["min_value"]
        unit = sensor["rate_params"]["unit"]
        rate_params = mean + "," +variance + "," + min_value + "," +unit

    if str(sensor["dist_rate"]) == "uniform" :
        lower_limit = sensor["rate_params"]["lower_limit"]
        upper_limit = sensor["rate_params"]["upper_limit"]
        unit = sensor["rate_params"]["unit"]
        rate_params = lower_limit + "," + upper_limit + "," + unit

    if str(sensor["dist_rate"]) == "poisson" :
        lmbda = sensor["rate_params"]["lambda"]
        min_value = sensor["rate_params"]["min_value"]
        unit = sensor["rate_params"]["unit"]
        rate_params = lmbda + "," + min_value + "," + unit

    if str(sensor["dist_rate"]) == "user_defined" :
        path = sensor["rate_params"]["path"]
        unit = sensor["rate_params"]["unit"]
        rate_params = path + "," + unit

    if str(sensor["dist_value"]) == "normal" :
        mean = sensor["value_params"]["mean"]
        variance = sensor["value_params"]["variance"]
        min_value = sensor["value_params"]["min_value"]
        value_params = mean + "," + variance + "," + min_value

    if str(sensor["dist_value"]) == "uniform" :
        lower_limit = sensor["value_params"]["lower_limit"]
        upper_limit = sensor["value_params"]["upper_limit"]
        value_params = lower_limit + "," + upper_limit

    if str(sensor["dist_value"]) == "poisson" :
        lmbda = sensor["value_params"]["lambda"]
        min_value = sensor["value_params"]["min_value"]
        value_params = lmbda + "," + min_value

    if str(sensor["dist_value"]) == "user_defined" :
        path = sensor["value_params"]["path"]
        #min_value = sensor["value_params"]["min_value"]
        value_params = path + "," + min_value

    params = [sensor_id, timestamp, sample_size, dist_rate, rate_params, dist_value, value_params]
    sensor_type = str(sensor["type"])
    sensor_types_dict[sensor_type] = params


print sensor_types_dict



for d in all_devices_list:
    print "Copying required binary and data files for device - {0}".format(d)
    #log_file.write("Creating sensors for device - {0} \n".format(d))
    vm_name = deployment_output[d]["host_vm_name"]
    host = container_vm[vm_name]["hostname_ip"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(hostname = host, username = user, pkey = k)

    command = [
        "sudo docker exec -i {0} bash -c 'mkdir -p {1}'".format(d,sensor_bin_path),
        "sudo docker exec -i {0} bash -c 'mkdir -p {1}'".format(d,sensor_data_path),
        "sudo docker cp -a {0}/bin {1}:/{2}".format(sensors_data_gen,d,sensor_path),
        "sudo docker cp -a {0}/data {1}:/{2}".format(sensors_data_gen,d,sensor_path)
        #"sudo docker exec -id {0} python {1}/sensor_data_host.py {2}".format(d,sensor_bin_path,device_ip[d])
    ]


    for cmd in command:
        stdin , stdout, stderr = c.exec_command(cmd)

    sensors = infra_config["devices"][d]["sensors"]
    sensor_dict_list = []
    sensor_txt = ""
    #Assuming 1 fog for each private network and fog is common to multiple private networks

    nw_name_list = deployment_output[d]["private_networks"].keys()
    device_ip = deployment_output[d]["private_networks"][nw_name_list[0]]

    for sensor in sensors:
        sensor_dict = {}
        sensor_type = sensor["sensor_type"]
        num_sensors = sensor["count"]
        link_list = []

        while num_sensors:
            sensor_file_name = sensor_type + "_" + str(num_sensors)
            sensor_txt += sensor_file_name +","
            link = "http://"+device_ip+":5000/sensors/"+sensor_file_name
            link_list.append(link)
            params = sensor_types_dict[sensor_type]
            command = "sudo docker exec -i {8} python {9}/data_gen.py {0} {1} {2} {3} {4} {5} {6} {7}".format(sensor_file_name,params[0],params[1],params[2],params[3],params[4],params[5],params[6],d,            sensor_bin_path)
            print command
            stdin , stdout, stderr = c.exec_command(command)
            num_sensors -= 1

        sensor_dict = {
            "sensor_type":sensor["sensor_type"],
            "links":link_list
            }
        sensor_dict_list.append(sensor_dict)

    sensor_txt = sensor_txt[:len(sensor_txt) -1]
    command = "sudo docker exec -id {0} python {1}/sensor_data_host.py {2} {3} '{4}'".format(d,sensor_bin_path,device_ip,sensor_data_path,sensor_txt)
    print command
    stdin,stdout, stderr = c.exec_command(command)
    print stdout,stderr

    c.close()

    deployment_output[d]["sensors"] = sensor_dict_list

print deployment_output




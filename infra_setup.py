import os
import paramiko
import random
import time
import json
from datetime import datetime
from threading import Thread

startTime = datetime.now()

#Init Variables

device_vm = {}
device_ip = {}
device_networks = {}

infra_config = json.load(open("config/infra_config.json"))
vm_config = json.load(open("config/vm_config.json"))
edge_devices = infra_config["devices"]["Edge"].keys()
fog_devices = infra_config["devices"]["Fog"].keys()
devices = fog_devices + edge_devices
private_networks_dict = infra_config["private_networks"]
public_networks_dict = infra_config["public_networks"]
partitions = json.load(open('dump/metis/metis_partitions.json'))
all_devices_list = json.load(open('dump/infra/all_devices_list.json'))
sensor_types = json.load(open("config/sensor_types.json"))

container_OS = infra_config["container_OS"]

container_vm = vm_config["container_host_VM"]
container_vm_names = container_vm.keys()

log_file = open("violet_log","w")

print
print
print ("**************************************************************************")
print ("                            DEPLOYING VIoLET                              ")
print ("**************************************************************************")
print
print

log_file.write("\n\n\n****************************************     DEPLOYING VIOLET       ****************************************\n")



"""
print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "             Copy data to other VMs            "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

for i in range(1,len(hosts)):
    for data in data_path_copy_vm:
        os.system("scp -i {0} {1} {2}@{3}:/home/{2}".format(key_path, data, user, hosts[i]))
"""


print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "             Copy data to other VMs            "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

data_path_copy_vm = [
    "sensors_data_gen/data_gen.py",
    "sensors_data_gen/sensor_data_host.py",
    "sensors_data_gen/data.csv",
    "sensors_data_gen/time.csv"
]

for i in range(len(container_vm_names)):
    for data in data_path_copy_vm:
        key_path = container_vm[container_vm_names[i]]["key_path"]
        user = container_vm[container_vm_names[i]]["user"]
        host = container_vm[container_vm_names[i]]["public_DNS"]
        os.system("scp -i {0} {1} {2}@{3}:/home/{2}".format(key_path, data, user, host))




print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "          Creating overlay networks            "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print
log_file.write("\n\n\n**************************************** CREATING OVERLAY NETWORKS ****************************************\n")

public_networks = public_networks_dict.keys()
host = container_vm[container_vm_names[0]]["public_DNS"]
user = container_vm[container_vm_names[0]]["user"]
key = container_vm[container_vm_names[0]]["key_path"]
k = paramiko.RSAKey.from_private_key_file(key)
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

c.connect( hostname = host, username = user, pkey = k)

public_networks = public_networks_dict.keys()
for i in public_networks:
        command = "sudo docker network create -d overlay {0}".format(str(i))
        print "Creating {0} network".format(str(i))
        log_file.write("Creating {0} network\n".format(str(i)))
        stdin , stdout, stderr = c.exec_command(command)
        log_file.write(stderr.read()+"\n")
        log_file.write(stdout.read()+"\n")

private_networks = private_networks_dict.keys()
for i in private_networks:
        command = "sudo docker network create -d overlay {0}".format(str(i))
        print "Creating {0} network".format(str(i))
        log_file.write("Creating {0} network \n".format(str(i)))
        stdin , stdout, stderr = c.exec_command(command)
        log_file.write(stderr.read()+"\n")
        log_file.write(stdout.read()+"\n")
c.close()

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "      Creating containers (IoT devices)        "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print

log_file.write("\n\n\n****************************************     CREATING CONTAINERS     ****************************************\n")

eth_port_map = {}

#CREATE FOG DEVICES
for f in fog_devices:
    device_type = infra_config["devices"]["Fog"][f]["device_type"]
    cpus = infra_config["fog_device_types"][device_type]["cpus"]
    commands = ["sudo docker run --ulimit nofile=50000:50000  -i -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v /tmp/work:/work --cpus={1}  --privileged --cap-add=NET_ADMIN --cap-add=NET_RAW --hostname {0} --name {0} {2} > /dev/null &".format(f,cpus,container_OS)]
    vm_index = int(partitions[f])
    vm_name = container_vm_names[vm_index]
    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    device_vm[f] = vm_name
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect(hostname = host, username = user, pkey = k,timeout=10)

    #Create entry in the eth_port_map
    #eth_port_map shows the eth port which is under use.
    #eth0 will be used by the bridge network to communicate with the outsied world
    eth_port = {}
    eth_port = {"bridge" : 0}
    eth_port_map[f] = eth_port

    eth_port_map[f]["eth_port_under_use"] = 0

    print "Creating {0} in {1}".format(f,vm_name)
    log_file.write("\n\nCreating {0} in {1}\n".format(f,vm_name))
    for command in commands:
        log_file.write(command+"\n")
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        log_file.write(stdout.read()+"\n")
        log_file.write(stderr.read()+"\n")

    c.close()

#CREATE EDGE DEVICES
for e in edge_devices:
    device_type = infra_config["devices"]["Edge"][e]["device_type"]
    cpus = infra_config["edge_device_types"][device_type]["cpus"]
    commands = ["sudo docker run --ulimit nofile=50000:50000  -i -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v /tmp/work:/work --cpus={1}  --privileged --cap-add=NET_ADMIN --cap-add=NET_RAW --hostname {0} --name {0} {2} > /dev/null &".format(e,cpus,container_OS)]
    vm_index = int(partitions[e])
    vm_name = container_vm_names[vm_index]
    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    device_vm[e] = vm_name
    c.connect(hostname = host, username = user, pkey = k)

    print "Creating {0} in {1}".format(e,vm_name)
    log_file.write("\n\nCreating {0} in {1} \n".format(e,vm_name))
    for command in commands:
        log_file.write(command)
        stdin, stdout, stderr = c.exec_command(command, timeout=5)
        log_file.write(stdout.read()+"\n")
        log_file.write(stderr.read()+"\n")

    c.close()

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "      Establishing network connectivity        "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print
log_file.write("\n\n\n***************************************ESTABLISHNING NETWORK CONNECTIVITY***************************************\n")


for d in all_devices_list:
    device_networks[d] = []

print "-------------------------"
print "Creating private networks"
print "-------------------------"

log_file.write("\n\n++++++++++ CREATING PRIVATE NETWORKS  ++++++++++\n")


private_network = private_networks_dict.keys()
for i in range(len(private_networks_dict)):
    gw = private_networks_dict[private_network[i]]["gw"]
    vm_name = device_vm[gw]
    host = container_vm[vm_name]["public_DNS"]
    user = container_vm[vm_name]["user"]
    key = container_vm[vm_name]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect(hostname = host, username = user, pkey = k)

    command = "sudo docker network connect {0} {1}".format(private_network[i],gw)
    device_networks[gw].append(private_network[i])
    print "Connecting {0} to {1}".format(gw,private_network[i])

    #eth1 will be used by the private network, to which the fog device acts as a gateway

    eth_port_map[gw]["eth_port_under_use"] += 1
    eth_port_map[gw][private_network[i]] = eth_port_map[gw]["eth_port_under_use"]

    log_file.write("Connecting {0} to {1} \n".format(gw,private_network[i]))
    stdin, stdout, stderr = c.exec_command(command)
    time.sleep(0.5)
    log_file.write("\n {0} \n {1}\n".format(stdout.read(), stderr.read()))

    command = "sudo docker exec -i {0} ip a | grep eth1 | awk 'FNR == 2 {{print $2}}'".format(gw)
    stdin, stdout, stderr = c.exec_command(command)
    ip = stdout.read()
    gw_ip = ip.replace(' ','')[:-4]
    #print "Gateway IP - {0}".format(gw_ip)
    device_ip[gw] = gw_ip

    commands = ["sudo docker exec -i {0} service iptables start".format(gw),"sudo docker exec -i {0} iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE".format(gw), "sudo docker exec -i {0} iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT".format(gw), "sudo docker exec -i {0} iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT".format(gw),"sudo docker exec -i {0} iptables -D INPUT -j REJECT --reject-with icmp-host-prohibited".format(gw),"sudo docker exec -i {0} iptables -D FORWARD -j REJECT --reject-with icmp-host-prohibited".format(gw)]
    for command in commands:
        stdin, stdout, stderr = c.exec_command(command)
    c.close()

    for j in range(len(private_networks_dict[private_network[i]]["conn_dev"])):
        device = private_networks_dict[private_network[i]]["conn_dev"][j]
        vm_name = device_vm[device]
        host = container_vm[vm_name]["public_DNS"]
        user = container_vm[vm_name]["user"]
        key = container_vm[vm_name]["key_path"]
        k = paramiko.RSAKey.from_private_key_file(key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        c.connect(hostname = host, username = user, pkey = k)

        print "Connecting {0} to {1}".format(device, private_network[i])
        log_file.write("Connecting {0} to {1}\n".format(device, private_network[i]))
        command = "sudo docker network connect {0} {1}".format(private_network[i],device)
        device_networks[device].append(private_network[i])
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        time.sleep(0.5)
        log_file.write("\n {0} \n {1}\n".format(stdout.read(), stderr.read()))

        command = "sudo docker network disconnect bridge {0}".format(device)
        c.exec_command(command,timeout=5)
        command = "sudo docker network disconnect docker_gwbridge {0}".format(device)
        c.exec_command(command,timeout=5)
        commands =["sudo docker exec -i {0} tc qdisc add dev eth1 handle 1: root htb default 11".format(device),"sudo docker exec -i {0} tc class add dev eth1 parent 1: classid 1:1 htb rate {1}Mbps".format(device, private_networks_dict[private_network[i]]["bw"]),"sudo docker exec -i {0} tc class add dev eth1 parent 1:1 classid 1:11 htb rate {1}Mbit".format(device,private_networks_dict[private_network[i]]["bw"]),"sudo docker exec -i {0} tc qdisc add dev eth1 parent 1:11 handle 10: netem delay {1}ms".format(device,int( private_networks_dict[private_network[i]]["latency"]))]
        log_file.write("Setting TC rules\n")
        for command in commands:
            stdin, stdout, stderr = c.exec_command(command,timeout=5)
            log_file.write(command+"\n")
            log_file.write(stdout.read()+"\n")
            log_file.write(stderr.read()+"\n")
            time.sleep(0.2)
        command = "sudo docker exec -i {0} ip route | grep default | awk '{{print $3}}'".format(device)
        stdin , stdout, stderr = c.exec_command(command,timeout=5)
        log_file.write(command+"\n")
        log_file.write(stdout.read()+"\n")
        log_file.write(stderr.read()+"\n")

        def_gw = stdout.read()
        def_gw = def_gw.replace(' ','')[:-1].upper()
        log_file.write("(Default GW) Changing to -> {1} \n".format(def_gw,gw_ip))
        command = "sudo docker exec -i {0} route del default gw {1}".format(device,def_gw)
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        command = "sudo docker exec -i {0} route add default gw {1}".format(device,gw_ip)
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        command = "sudo docker exec -i {0} ip a | grep eth1 | awk 'FNR == 2 {{print $2}}'".format(device)
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        time.sleep(.5)
        ip = stdout.read()
        ip = ip.replace(' ','')[:-4]
        #print "Device({0}) IP - {1}".format(device,ip)
        device_ip[device]=ip

        command = "sudo docker exec -i {0} ip a".format(device)
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        log_file.write("\n@@@@@@@@@@@@@@@@+++++++++++++++++++++@@@@@@@@@@@@@@@@@@@\n")
        log_file.write(stdout.read())
        command = "sudo docker exec -i {0} ip route".format(device)
        stdin, stdout, stderr = c.exec_command(command,timeout=5)
        log_file.write(stdout.read()+"\n")
        log_file.write("@@@@@@@@@@@@@@@@+++++++++++++++++++++@@@@@@@@@@@@@@@@@@\n")
        c.close()

print "------------------------"
print "Creating public networks"
print "------------------------"


log_file.write("\n\n++++++++++ CREATING PUBLIC NETWORKS  ++++++++++\n")

public_network = public_networks_dict.keys()
for i in range(len(public_networks_dict)):
    for j in range(len(public_networks_dict[public_network[i]]["conn_dev"])):
        device = public_networks_dict[public_network[i]]["conn_dev"][j]
        vm_name = device_vm[device]
        host = container_vm[vm_name]["public_DNS"]
        user = container_vm[vm_name]["user"]
        key = container_vm[vm_name]["key_path"]
        k = paramiko.RSAKey.from_private_key_file(key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        c.connect(hostname = host, username = user, pkey = k)

        command = "sudo docker network connect {} {}".format(public_network[i],device)

        eth_port_map[device]["eth_port_under_use"] += 1
        eth_port_map[device][public_network[i]] = eth_port_map[device]["eth_port_under_use"]

        device_networks[device].append(public_network[i])
        print "Connecting {0} to {1}".format(device, public_network[i])
        log_file.write("Connecting {0} to {1} \n".format(device, public_network[i]))
        stdin , stdout, stderr = c.exec_command(command,timeout=5)
        time.sleep(0.5)
        log_file.write("\n {0} \n {1}\n".format(stdout.read(), stderr.read()))

        command = "sudo docker network disconnect docker_gwbridge {0}".format(device)
        c.exec_command(command,timeout=5)

        eth_port = eth_port_map[device][public_network[i]]
        commands =[
        "sudo docker exec -i {0} tc qdisc add dev eth{1} handle 1: root htb default 11".format(device,eth_port),
        "sudo docker exec -i {0} tc class add dev eth{1} parent 1: classid 1:1 htb rate {2}Mbps".format(device, eth_port, public_networks_dict[public_network[i]]["bw"]),
        "sudo docker exec -i {0} tc class add dev eth{1} parent 1:1 classid 1:11 htb rate {2}Mbit".format(device, eth_port, public_networks_dict[public_network[i]]["bw"]),
        "sudo docker exec -i {0} tc qdisc add dev eth{1} parent 1:11 handle 10: netem delay {2}ms".format(device, eth_port, int( public_networks_dict[public_network[i]]["latency"]))
        ]

        log_file.write("Setting TC rules\n")
        for command in commands:
            stdin, stdout, stderr = c.exec_command(command,timeout=5)
            log_file.write(command+"\n")
            log_file.write(stdout.read()+"\n")
            log_file.write(stderr.read()+"\n")
            time.sleep(0.2)


        c.close()

print
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print "           Create sensors                      "
print "+++++++++++++++++++++++++++++++++++++++++++++++"
print
log_file.write("\n\n\n****************************************      CREATING SENSORS      ****************************************\n")

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
        rate_params = mean + "," +variance

    if str(sensor["dist_rate"]) == "uniform" :
        lower_limit = sensor["rate_params"]["lower_limit"]
        upper_limit = sensor["rate_params"]["upper_limit"]
        rate_params = lower_limit + "," + upper_limit

    if str(sensor["dist_rate"]) == "poisson" :
        lmbda = sensor["rate_params"]["lambda"]
        rate_params = lmbda

    if str(sensor["dist_rate"]) == "user_defined" :
        path = sensor["rate_params"]["path"]
        rate_params = path

    if str(sensor["dist_value"]) == "normal" :
        mean = sensor["value_params"]["mean"]
        variance = sensor["value_params"]["variance"]
        value_params = mean + "," + variance

    if str(sensor["dist_value"]) == "uniform" :
        lower_limit = sensor["value_params"]["lower_limit"]
        upper_limit = sensor["value_params"]["upper_limit"]
        value_params = lower_limit + "," + upper_limit

    if str(sensor["dist_value"]) == "poisson" :
        lmbda = sensor["value_params"]["lambda"]
        value_params = lmbda

    if str(sensor["dist_value"]) == "user_defined" :
        path = sensor["value_params"]["path"]
        value_params = path

    params = [sensor_id, timestamp, sample_size, dist_rate, rate_params, dist_value, value_params]
    sensor_type = str(sensor["type"])
    sensor_types_dict[sensor_type] = params



edge_count = len(edge_devices)


devices_with_sensors = {}
sensor_link = {}

for n in private_networks_dict:
    fog=private_networks_dict[n]["gw"]
    fog_ip = device_ip[fog]
    #print fog_ip
    linklist=[]
    #print linklist

    edge_dev = private_networks_dict[n]["conn_dev"]
    for e in edge_dev:
        print "Creating sensors for device - {0}".format(e)
        log_file.write("Creating sensors for device - {0} \n".format(e))
        s = []
        sensor_index = 1
        e_sensors = infra_config["devices"]["Edge"][e]["sensors"].keys()
        vm_name = device_vm[e]
        host = container_vm[vm_name]["public_DNS"]
        user = container_vm[vm_name]["user"]
        key = container_vm[vm_name]["key_path"]
        k = paramiko.RSAKey.from_private_key_file(key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname = host, username = user, pkey = k)

        command = [
            "sudo docker cp {0} {1}:/".format("data_gen.py",e),
            "sudo docker cp {0} {1}:/".format("sensor_data_host.py",e),
            "sudo docker cp {0} {1}:/".format("data.csv",e),
            "sudo docker cp {0} {1}:/".format("time.csv",e),
            "sudo docker exec -id {0} python sensor_data_host.py {1}".format(e,device_ip[e])
        ]

        for cmd in command:
            stdin , stdout, stderr = c.exec_command(cmd)

        c.close()


        vm_name = device_vm[e]
        host = container_vm[vm_name]["public_DNS"]
        user = container_vm[vm_name]["user"]
        key = container_vm[vm_name]["key_path"]
        k = paramiko.RSAKey.from_private_key_file(key)
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(hostname = host, username = user, pkey = k)

        for e_sensor in e_sensors:
            num_sensors = infra_config["devices"]["Edge"][e]["sensors"][e_sensor]
            for i in range(1,int(num_sensors)+1):
                sensor_file_name = e+"_"+e_sensor+"_"+str(sensor_index)
                s.append(sensor_file_name)
                link = "http://"+device_ip[e]+":5000/sensors/"+sensor_file_name
                linklist.append(link)
                params = sensor_types_dict[e_sensor]
                command = "sudo docker exec -i {8} python data_gen.py {0} {1} {2} {3} {4} {5} {6} {7}".format(sensor_file_name,params[0],params[1],params[2],params[3],params[4],params[5],params[6],e)
                stdin , stdout, stderr = c.exec_command(command)
                sensor_index += 1
        c.close()

        devices_with_sensors[e]=s
    #print len(linklist)
    sensor_link[fog] = linklist


log_file.close()
with open('dump/infra/infra_device_vm.json', 'w') as file:
     file.write(json.dumps(device_vm))
with open('dump/infra/infra_fog_devices.json','w') as file:
    file.write(json.dumps(fog_devices))
with open('dump/infra/infra_edge_devices.json','w') as file:
    file.write(json.dumps(edge_devices))
with open('dump/infra/infra_devices_with_sensors.json','w') as file:
    file.write(json.dumps(devices_with_sensors))
with open('dump/infra/eth_port_map.json','w') as file:
    file.write(json.dumps(eth_port_map))
with open('dump/infra/infra_device_networks.json','w') as file:
    file.write(json.dumps(device_networks))
with open('dump/infra/infra_device_ip.json', 'w') as file:
     file.write(json.dumps(device_ip))
with open('dump/infra/infra_devices.json', 'w') as file:
     file.write(json.dumps(devices))
with open('dump/infra/infra_pvt.json', 'w') as file:
     file.write(json.dumps(private_networks_dict))
with open('dump/infra/infra_pub.json', 'w') as file:
     file.write(json.dumps(public_networks_dict))
with open('dump/infra/infra_fog_sensor_link.json','w') as file:
    file.write(json.dumps(sensor_link))

print datetime.now() - startTime

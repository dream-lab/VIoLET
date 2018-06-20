import json
import random
import sys

num_devices = int(sys.argv[1])
num_pvt_networks = int(sys.argv[2])
edge_device_types_count = sys.argv[3]
fog_device_types_count = sys.argv[4]
num_sensors_per_device = int(sys.argv[5])
edge_denisty =int(sys.argv[6])
container_OS = sys.argv[7]


edge_device_types_count = edge_device_types_count.split(",")
fog_device_types_count = fog_device_types_count.split(",")

print edge_device_types_count
print fog_device_types_count

num_edge_devices = num_devices - num_pvt_networks
num_edge_per_network = (num_edge_devices/num_pvt_networks)
remanant = num_edge_devices % num_pvt_networks

devices_meta = {}

infra_config = {}

infra_config["container_OS"] = container_OS
device_types = json.load(open("config/device_types.json"))
edge_device_types = device_types["edge_device_types"]
fog_device_types = device_types["fog_device_types"]
sensor_types = json.load(open("config/sensor_types.json"))

infra_config["edge_device_types"] = edge_device_types
infra_config["fog_device_types"] = fog_device_types
infra_config["sensor_types"] = sensor_types
devices_meta = {}

devices_meta["device_count"] = num_devices
Edge = {}
Edge["edge_device_count"] = num_edge_devices
e_type = edge_device_types.keys()
j = 0
for  i in e_type:
    e = {}
    e["cpus"] = edge_device_types[i]["cpus"]
    e["count"] = int(edge_device_types_count[j])
    j += 1
    Edge[i] = e

Fog = {}
Fog["fog_device_count"] = num_pvt_networks
f_type = fog_device_types.keys()
j = 0
for i in f_type:
    f = {}
    f["cpus"] = fog_device_types[i]["cpus"]
    f["count"] = int(fog_device_types_count[j])
    j += 1
    #f["count"] = input("Number of {0} devices?\n".format(i))
    Fog[i] = f
devices_meta["Edge"] = Edge
devices_meta["Fog"] = Fog

print devices_meta

#with open('dump/topo_devices_meta', 'w') as fd:
#     fd.write(json.dumps(devices_meta))



print
print
print "Creating infra-config . Path =  VIoLET/config/infra_config.json"
print "Done"

devices = {}
fog_types = []
edge_types = []
fog_devices = {}
edge_devices = {}
all_devices_list = []

#CREATE FOG DEVICES
fog_types = devices_meta["Fog"].keys()
device_index = 1
for i in range(1,len(fog_types)):
    fog_type = fog_types[i]
    fog_type_count = devices_meta["Fog"][fog_type]["count"]
    for j in range(fog_type_count):
        device_type = {}
        fog_name = "Fog-{0}".format(device_index)
        all_devices_list.append(fog_name)
        device_index += 1
        device_type["device_type"] = fog_type
        fog_devices[fog_name] = device_type
devices["Fog"] = fog_devices

#CREATE EDGE DEVICES
edge_types = devices_meta["Edge"].keys()
subnet_index = 1
device_index = 1

#CREATE SENSORS
sensors = json.load(open("config/sensor_types.json"))
sensor_types = []
for i in range(len(sensors["sensor_types"])):
    sensor_types.append(sensors["sensor_types"][i]["type"])

num_sensors = int(num_sensors_per_device / len(sensor_types))
rem = num_sensors + (num_sensors_per_device % len(sensor_types))
device_sensors = {}
for i in range(len(sensor_types)):
    if i == (len(sensor_types) - 1):
        device_sensors[sensor_types[i]] = str(rem)
    else:
        device_sensors[sensor_types[i]] = str(num_sensors)

for i in range(1,len(edge_types)):
    edge_type = edge_types[i]
    edge_type_count = devices_meta["Edge"][edge_type]["count"]
    for j in range(edge_type_count):
        device_type = {}
        edge_name = "Edge-{0}.{1}".format(subnet_index,device_index)
        all_devices_list.append(edge_name)
        if (device_index == num_edge_per_network):
            device_index = 1
            subnet_index += 1
        else:
            device_index += 1
        device_type["device_type"] = edge_type
        edge_devices[edge_name] = device_type
        edge_devices[edge_name]["sensors"] = device_sensors
devices["Edge"] = edge_devices
infra_config["devices"] = devices

num_edge_per_network = (num_edge_devices/num_pvt_networks)

#Create private networks
private_networks_dict = {}
BW = ["5","10","25","50"]
LATENCY = ["20","40","100","200"]
conn_dev = []
p = {}
for i in range(1, num_pvt_networks+1):
    p = {}
    conn_dev = []
    pvt = "violet_private_{0}".format(i)
    gw = "Fog-{0}".format(i)
    bw = BW[random.randint(0,3)]
    latency = LATENCY[random.randint(0,3)]
    if(i == num_pvt_networks and remanant != 0):
        num_edge_per_network += remanant
    for j in range(1, num_edge_per_network+1):
        e = "Edge-{0}.{1}".format(i,j)
        conn_dev.append(e)
    p["gw"] = gw
    p["bw"] = bw
    p["latency"] = latency
    p["conn_dev"] = conn_dev
    private_networks_dict[pvt]=p
infra_config["private_networks"] = private_networks_dict

#Create public networks
public_networks_dict = {}
BW = ["25","50","125","250"]
LATENCY = ["5","20","50","100"]
p = {}
conn_dev = []
pub = "violet_public_{0}".format(1)
bw = BW[random.randint(0,3)]
latency = LATENCY[random.randint(0,3)]
conn_dev = fog_devices.keys()
p["bw"] = bw
p["latency"] = latency
p["conn_dev"] = conn_dev
public_networks_dict[pub] = p
infra_config["public_networks"] = public_networks_dict

with open('config/infra_config.json', 'w') as fd:
    fd.write(json.dumps(infra_config))
with open('dump/infra/all_devices_list.json','w') as fd:
    fd.write(json.dumps(all_devices_list))

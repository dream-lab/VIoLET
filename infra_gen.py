import json
import random
import sys

#Global Variables
num_edge_devices = 0
num_fog_devices = 0
edge_device_types_dict = {}
fog_device_types_dict = {}
all_devices_list = []

ports = range(1025,65535)
i=1
sensor_types = json.load(open("config/sensor_types.json"))
sensor_types_list = sensor_types["sensor_types"]
sensors_list = []
for sensor in sensor_types_list:
    print i
    sensors_list.append(sensor["type"])

print sensors_list

num_devices = int(sys.argv[i])
i+=1
num_pvt_networks = int(sys.argv[i])
i+=1
num_device_types = int(sys.argv[i])
i+=1
for n in range(num_device_types):
    device_name = sys.argv[i]
    i+=1
    edge_count = int(sys.argv[i])
    if edge_count != 0:
        edge_device_types_dict[device_name] = edge_count
    num_edge_devices += edge_count
    i+=1
    fog_count = int(sys.argv[i])
    if fog_count !=0:
        fog_device_types_dict[device_name] = fog_count
    num_fog_devices += fog_count
    i+=1

num_sensors_per_device = int(sys.argv[i])
i+=1

print num_edge_devices,num_fog_devices

if num_devices != (num_edge_devices + num_fog_devices):
    print "Incorrect Initialization"
    exit(0)



num_edge_per_network = (num_edge_devices/num_pvt_networks)
remanant = num_edge_devices % num_pvt_networks


print edge_device_types_dict
print fog_device_types_dict


#edge_device_types_list = edge_device_types_dict.keys()
#fog_device_types_list = fog_device_types_dict.keys()


print
print
print "Creating infra_config.json"
print "Path = VIoLET/config/infra_config.json"
print "..."
print


infra_config = {}
devices = {}
private_networks = {}


def create_sensors():
    sensors = []
    sensors_dict = {}
    for n in range(num_sensors_per_device):
        sensor_type = random.choice(sensors_list)
        if sensor_type in sensors_dict:
            sensors_dict[sensor_type] += 1
        else:
            sensors_dict[sensor_type] = 1
    for sensor_type in sensors_dict:
        sensor = {
            "sensor_type": sensor_type,
            "count" : sensors_dict[sensor_type]
            }
        sensors.append(sensor)
    return sensors


#Creating Fog Devices
fog_index = 1
for i in range(num_fog_devices):
    fog_type=random.choice(fog_device_types_dict.keys())
    #print fog_type
    fog_name = "Fog-{0}".format(fog_index)
    port = random.choice(ports)
    all_devices_list.insert(len(all_devices_list), fog_name)
    sensors = create_sensors()
    devices[fog_name] = {
        "device_type": fog_type,
        "sensors": sensors,
        "port":port
    }
    fog_index += 1
    fog_device_types_dict[fog_type] -= 1
    if fog_device_types_dict[fog_type] == 0:
        fog_device_types_dict.pop(fog_type)



#Creating Edge Devices
pvt_network_index = 1
lat_edge_index = 1
for i in range(num_pvt_networks):
    edge_index = 1
    for j in range(num_edge_per_network):
        edge_type = random.choice(edge_device_types_dict.keys())
        #print edge_type
        edge_name = "Edge-{0}.{1}".format(pvt_network_index, edge_index)
        port = random.choice(ports)
        all_devices_list.insert(len(all_devices_list), edge_name)
	sensors = create_sensors()
        devices[edge_name] = {
            "device_type": edge_type,
            "sensors": sensors,
            "port": port
        }
        edge_index += 1
        edge_device_types_dict[edge_type] -= 1
        if edge_device_types_dict[edge_type] == 0:
            edge_device_types_dict.pop(edge_type)
    pvt_network_index += 1
    last_edge_index = edge_index

pvt_network_index = 1
#last_edge_index += 1
for i in range(remanant):
    edge_type = random.choice(edge_device_types_dict.keys())
    edge_name = "Edge-{0}.{1}".format(pvt_network_index, last_edge_index)
    port = random.choice(ports)
    all_devices_list.append(edge_name)
    sensors = create_sensors()
    devices[edge_name] = {
        "device_type": edge_type,
        "sensors": sensors,
        "port": port
    }
    pvt_network_index += 1
    edge_device_types_dict[edge_type] -= 1
    if edge_device_types_dict[edge_type] == 0:
        edge_device_types_dict.pop(edge_type)




infra_config["devices"] = devices
#print devices.keys()


#Create Private Networks
pvt_networks_dict = {}
#initialization
BW = ["5","10","25","50"]
LAT = ["20","40","100","200"]

private_ip_range = "192.168."
public_ip_range = "10.0."

pvt_network_index = 1
for i in range(num_pvt_networks):
    conn_dev = []
    pvt_network_name = "violet_private_{0}".format(pvt_network_index)
    gw = "Fog-{0}".format(pvt_network_index)
    bw = random.choice(BW)
    lat = random.choice(LAT)
    for device in devices.keys():
	if "Edge-{0}".format(pvt_network_index) in device:
	    #print device
	    conn_dev.append(device)
    pvt_networks_dict[pvt_network_name] = {
    "subnet": private_ip_range+str(pvt_network_index)+".0/24",
    "ip_range": private_ip_range+str(pvt_network_index)+".0/24",
	"gateway":gw,
	"latency_ms":lat,
	"bandwidth_mbps":bw,
	"devices":conn_dev
    }
    pvt_network_index += 1


infra_config["private_networks"] = pvt_networks_dict

#print pvt_networks_dict

#Create Public Networks
pub_networks_dict = {}
#initialization
BW = ["25","50","125","250"]
LAT = ["5","20","50","100"]

pub_network_index = 1
conn_dev = []
pub_network_name = "violet_public_{0}".format(pub_network_index)
bw = random.choice(BW)
lat = random.choice(LAT)
for device in devices.keys():
    if "Fog" in device:
        #print device
        conn_dev.append(device)
pub_networks_dict[pub_network_name] = {
    "subnet": public_ip_range+str(pub_network_index)+".0/24",
    "ip_range": public_ip_range+str(pub_network_index)+".0/24",
    "gateway":gw,
    "latency_ms":lat,
    "bandwidth_mbps":bw,
    "devices":conn_dev
}
pub_network_index += 1

infra_config["public_networks"] = pub_networks_dict


lat = random.choice(LAT)
bw = random.choice(BW)
#conn_dev = []
#print conn_dev

infra_config["public_global_network"] = {
    "latency_ms": lat,
    "bandwidth_mbps": bw,
    "devices": conn_dev,
    "subnet": public_ip_range+str(pub_network_index)+".0/24",
    "ip_range": public_ip_range+str(pub_network_index)+".0/24"
}

infra_config["block_network_route"] = []




#print pub_networks_dict

print "done."


with open('config/infra_config.json', 'w') as fd:
    fd.write(json.dumps(infra_config))
with open('dump/infra/all_devices_list.json','w') as fd:
    fd.write(json.dumps(all_devices_list))



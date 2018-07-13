import json
import random


infra_gen_dict = json.load(open("config/infra_gen.json"))
public_networks_dict=infra_gen_dict["public_networks"]
private_networks_dict=infra_gen_dict["private_networks"]
network=infra_gen_dict["network"]

pub_bandwidth_mbps = network["public_networks"]["bandwidth_mbps"]
pub_latency_ms = network["public_networks"]["latency_ms"]

pvt_bandwidth_mbps = network["private_networks"]["bandwidth_mbps"]
pvt_latency_ms = network["private_networks"]["latency_ms"]


sensor_types=json.load(open("config/sensor_types.json"))
sensor_types_list = sensor_types["sensor_types"]





print
print
print "Creating infra_config.json"
print "Path = VIoLET/config/infra_config.json"
print "..."
print

infra_config = {}
devices = {}
pub_network_dict = {}
pvt_network_dict = {}
all_devices_list = []
device_type_fog_dict = {}


ports = range(1025,65535)

sensors_list = []
for sensor in sensor_types_list:
    sensors_list.append(sensor["type"])

print sensors_list


def create_sensors(num_sensors):
    sensors = []
    sensors_dict = {}
    for n in range(num_sensors):
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


def create_device(port,device_type,num_sensors):
    device = {
        "device_type":device_type,
        "port":port,
        "sensors":create_sensors(num_sensors)
    }
    return device

public_ip_range = "10.0."
pub_network_index = 1
conn_dev=[]
for p in public_networks_dict.keys():
    index = 1
    pub_network_name = p
    #conn_dev = []
    bw = random.choice(pub_bandwidth_mbps)
    lat = random.choice(pub_latency_ms)
    devices_list = public_networks_dict[p]
    for d in devices_list:
        device_type = d["device_type"]
        device_type_fog_list = []
        number_devices = d["number_devices"]
        num_sensors = int(d["number_sensors"])
        for n in range(int(number_devices)):
            device_name = "Fog-{0}".format(index)
            port = random.choice(ports)
            devices[device_name] = create_device(port,device_type,num_sensors)
            all_devices_list.append(device_name)
            conn_dev.append(device_name)
            device_type_fog_list.append(device_name)
            index+=1
        device_type_fog_dict[device_type] = device_type_fog_list
    pub_network_dict[pub_network_name] = {
        "subnet": public_ip_range+str(pub_network_index)+".0/24",
        "ip_range": public_ip_range+str(pub_network_index)+".0/24",
        "gateway":random.choice(conn_dev),
        "latency_ms":lat,
        "bandwidth_mbps":bw,
        "devices":conn_dev
    }
    pub_network_index += 1

infra_config["public_networks"] = pub_network_dict

bw = random.choice(pub_bandwidth_mbps)
lat = random.choice(pub_latency_ms)

infra_config["public_global_network"] = {
    "latency_ms": lat,
    "bandwidth_mbps": bw,
    "devices": conn_dev,
    "subnet": public_ip_range+str(pub_network_index)+".0/24",
    "ip_range": public_ip_range+str(pub_network_index)+".0/24"
}



private_ip_range = "192.168."
pvt_network_index = 1
for p in private_networks_dict.keys():
    index = 1
    pvt_network_name = p
    conn_dev = []
    bw = random.choice(pvt_bandwidth_mbps)
    lat = random.choice(pvt_latency_ms)
    gw_device_type = private_networks_dict[p]["gateway_device_type"]
    gw = random.choice(device_type_fog_dict[gw_device_type])
    device_type_fog_dict[gw_device_type].remove(gw)
    device_type = private_networks_dict[p]["device_type"]
    number_devices = private_networks_dict[p]["number_devices"]
    num_sensors = int(private_networks_dict[p]["number_sensors"])
    for n in range(int(number_devices)):
        device_name = "Edge-{0}.{1}".format(pvt_network_index,index)
        port = random.choice(ports)
        devices[device_name] = create_device(port,device_type,num_sensors)
        all_devices_list.append(device_name)
        conn_dev.append(device_name)
        index += 1
    pvt_network_dict[pvt_network_name] = {
        "subnet": private_ip_range+str(pvt_network_index)+".0/24",
        "ip_range": private_ip_range+str(pvt_network_index)+".0/24",
        "gateway":gw,
        "latency_ms":lat,
        "bandwidth_mbps":bw,
        "devices":conn_dev
    }

    pvt_network_index +=1

infra_config["private_networks"]=pvt_network_dict

infra_config["devices"] = devices

infra_config["block_network_route"] = []

with open('config/infra_config.json', 'w') as fd:
    fd.write(json.dumps(infra_config))
with open('dump/infra/all_devices_list.json','w') as fd:
    fd.write(json.dumps(all_devices_list))




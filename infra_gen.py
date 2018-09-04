import json
import random
import sys
import getopt

infra_gen_dict = json.load(open("config/infra_gen.json"))
public_networks_dict=infra_gen_dict["public_networks"]
private_networks_dict=infra_gen_dict["private_networks"]
network=infra_gen_dict["network"]

pub_bandwidth_mbps = network["public_networks"]["bandwidth_mbps"]
pub_latency_ms = network["public_networks"]["latency_ms"]
pub_window_size = float(network["public_networks"]["window_size_bits"]) / 1000

pvt_bandwidth_mbps = network["private_networks"]["bandwidth_mbps"]
pvt_latency_ms = network["private_networks"]["latency_ms"]
pvt_window_size = float(network["private_networks"]["window_size_bits"]) / 1000

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
nw_device_type_fog_dict = {}

seed = 10
logic = 0

def main(argv):
    global seed,logic
    try:
	opts, args = getopt.getopt(argv,"s:l:",["seed=","logic="])
    except getopt.GetoptError:
	print 'python infra_gen.py -s <seed_value> -l <logic_value>'
	sys.exit(2)
    for opt, arg in opts:
	if opt in ("-s","--seed"):
	    seed = arg
	    print "Seed value = ",seed
	if opt in ("-l","--logic"):
	    logic = arg
	    print "Logic value = ",logic
	

if __name__ == "__main__":
   main(sys.argv[1:])



min_port = 32768
max_port = 60999

print "Port ranges from {0} to {1}".format(min_port,max_port)

ports = range(min_port,max_port)

#try:
#    seed = sys.argv[1]
#except IndexError:
#    seed = 500
#    print "seed not given, will generate random bandwidth and latency combination for network"

#print "seed=",seed



bw_lat = [(20,5),(40,5),(60,5),(80,5),(100,5),(20,25),(40,25),(60,25),(80,25),(100,25),(20,50),(40,50),(20,75)]

if logic == "1":
	print 
	print "BW_Lat pairs"
	print bw_lat
	print "The above combination of bw_lat pairs will be used for the networks"


r = random.Random(seed)

sensors_list = []
for sensor in sensor_types_list:
    sensors_list.append(sensor["type"])

print
print "Sensor types: ", sensors_list
print

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
    #bw = random.choice(pub_bandwidth_mbps)
    
    if logic == "1":
	bw,lat = r.choice(bw_lat)
    else:
    	lat = r.choice(pub_latency_ms)
    	#print "pub_latency_ms for {0} is {1}".format(p,lat)
    	print
    	peak_bw = pub_window_size/float(lat)
    	pub_bw = []
    	for bw in pub_bandwidth_mbps:
		if float(bw) < peak_bw:
		    pub_bw.append(bw)
    	bw = min(pub_bandwidth_mbps)
    	try:
    	    bw = r.choice(pub_bw)
    	except IndexError:
		print "The latency choosen is not a valid choice as bandwidth depends on it as well as window size"
		print "Please change the infra_gen.json to retry or run again for correct results"
		print "Default value of bw is set to the minimum of the available bandwidth"
                #print "pub_bandwidth_mbps for {0} is {1}".format(p,bw)
    
    print "pub_bandwidth_mbps for {0} is {1}".format(p,bw) 
    print "pub_latency_ms for {0} is {1}".format(p,lat)
    print
    devices_list = public_networks_dict[p]["devices"]
    print devices_list
    device_type_fog_dict = {}
    conn_dev = []
    for d in devices_list:
        device_type = d["device_type"]
        device_type_fog_list = []
        number_devices = d["number_devices"]
        num_sensors = int(d["number_sensors"])
	device_type_fog_list = []
        for n in range(int(number_devices)):
            device_name = "Fog-{0}.{1}".format(pub_network_index,index)
            port = r.choice(ports)
            devices[device_name] = create_device(port,device_type,num_sensors)
            all_devices_list.append(device_name)
            conn_dev.append(device_name)
            device_type_fog_list.append(device_name)
            index+=1
        device_type_fog_dict[device_type] = device_type_fog_list
    nw_device_type_fog_dict[p] = device_type_fog_dict
    pub_network_dict[pub_network_name] = {
        "subnet": public_ip_range+str(pub_network_index)+".0/24",
        "ip_range": public_ip_range+str(pub_network_index)+".0/24",
        #"gateway":random.choice(conn_dev),
        "latency_ms":lat,
        "bandwidth_mbps":bw,
        "devices":conn_dev
    }
    print "conn ",conn_dev
    pub_network_index += 1

infra_config["public_networks"] = pub_network_dict

print nw_device_type_fog_dict

#bw = random.choice(pub_bandwidth_mbps)

if logic == "1":
    bw,lat = r.choice(bw_lat)
else:
    lat = r.choice(pub_latency_ms)
    #print "pub_latency_ms for {0} is {1}".format("public_global_network",lat)
    #print
    peak_bw = pub_window_size/float(lat)
    pub_bw = []
    for bw in pub_bandwidth_mbps:
        if float(bw) < peak_bw:
            pub_bw.append(bw)

    bw = min(pub_bandwidth_mbps)
    try:
        bw = r.choice(pub_bw)
    except IndexError:
        print "The latency choosen is not a valid choice as bandwidth depends on it as well as window size"
        print "Please change the infra_gen.json to retry or run again for correct results"
        print "Default value of bw is set to the minimum of the available bandwidth"

print "pub_bandwidth_mbps for {0} is {1}".format("public_global_network",bw)
print "pub_latency_ms for {0} is {1}".format("public_global_network",lat)
print


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
    #bw = random.choice(pvt_bandwidth_mbps)
    if logic == "1":
	bw,lat = r.choice(bw_lat)
    else:
    	lat = r.choice(pvt_latency_ms)
    	#print "pvt_latency_ms for {0} is {1}".format(p,lat)
    	#print
    	peak_bw = pvt_window_size/float(lat)
    	pvt_bw = []
    	for bw in pvt_bandwidth_mbps:
    	    if float(bw) < peak_bw:
    	        pvt_bw.append(bw)
	
	bw = min(pvt_bandwidth_mbps)
    	try:
        	bw = r.choice(pvt_bw)
    	except IndexError:
        	print "The latency choosen is not a valid choice as bandwidth depends on it as well as window size"
        	print "Please change the infra_gen.json to retry or run again for correct results"
        	print "Default value of bw is set to the minimum of the available bandwidth"

    
    print "pvt_bandwidth_mbps for {0} is {1}".format(p,bw)
    print "pvt_latency_ms for {0} is {1}".format(p,lat)
    print
    
    for pb in public_networks_dict.keys():
	if p in public_networks_dict[pb]["private_networks_list"]:
		break;

    #nw = nw_device_type_fog_dict[pb]
    gw_device_type = private_networks_dict[p]["gateway_device_type"]
    print nw_device_type_fog_dict[pb]
    gw = nw_device_type_fog_dict[pb][gw_device_type][0]
    nw_device_type_fog_dict[pb][gw_device_type].remove(gw)
    device_type = private_networks_dict[p]["device_type"]
    number_devices = private_networks_dict[p]["number_devices"]
    num_sensors = int(private_networks_dict[p]["number_sensors"])
    for n in range(int(number_devices)):
        device_name = "Edge-{0}.{1}".format(pvt_network_index,index)
        port = r.choice(ports)
	#ports.remove(port)
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


#if __name__ == "__main__":
#   main(sys.argv[1:])


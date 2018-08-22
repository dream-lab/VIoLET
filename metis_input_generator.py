import json
import sys
device_networks = {}
public_networks = {}
private_networks = {}
metis_input = {}
vm_types = json.load(open('config/vm_types.json'))
vm_config = json.load(open('config/vm_config.json'))
infra_config = json.load(open('config/infra_config.json'))
all_devices_list= infra_config["devices"].keys()
#print all_devices_list
print "\n\nGenerating metis input\n\n"
device_types = json.load(open('config/device_types.json'))

meta_vertex = {}
meta_devices = []

container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()

print "Considering all VMs are same and similar latency across all the VMs\n"
vm_type = container_vm[container_vm_names[0]]["vm_type"]
print vm_type
print


for d in all_devices_list:
    device_networks[d] = {}
    device_networks[d]["private"] = []
    device_networks[d]["public"] = []



public_networks = infra_config["public_networks"]

for p in public_networks:
    conn_dev = public_networks[p]["devices"]
    for d in conn_dev:
        device_networks[d]["public"].append(p)



private_networks = infra_config["private_networks"]

#info = {}
#networks = []
#connections = {}
#meta_index = 0

for p in private_networks:
    latency = float(private_networks[p]["latency_ms"])
    out_latency_ms = float(vm_types[vm_type]["out_latency_ms"])
    conn_dev = private_networks[p]["devices"]
    if latency < out_latency_ms:
	for d in conn_dev:
	    all_devices_list.remove(d)
	

for p in private_networks:
    gw = private_networks[p]["gateway"]
    device_networks[gw]["private"].append(p)
    conn_dev = private_networks[p]["devices"]
    for d in conn_dev:
        device_networks[d]["private"].append(p)
    latency = float(private_networks[p]["latency_ms"])
    out_latency_ms = float(vm_types[vm_type]["out_latency_ms"])
    #print latency,out_latency_ms
    coremark = 0
    memory_mb = 0
    disk_mb = 0
    info = {}
    networks = []
    connections = {}

    if latency < out_latency_ms:
	if p not in meta_vertex: meta_vertex[p] = {}
	meta_vertex[p]["devices"] = conn_dev
	meta_vertex[p]["gateway"] = gw
	meta_devices.append(gw)
	for d in conn_dev:
	    device_type = infra_config["devices"][d]["device_type"]
	    coremark += int(device_types[device_type]["coremark"])
    	    memory_mb += int(device_types[device_type]["memory_mb"])
    	    disk_mb += int(device_types[device_type]["disk_mb"])
	    #all_devices_list.remove(d)
	    meta_devices.append(d)
	device_type = infra_config["devices"][gw]["device_type"]
	coremark += int(device_types[device_type]["coremark"])
        memory_mb += int(device_types[device_type]["memory_mb"])
        disk_mb += int(device_types[device_type]["disk_mb"])
	#print p,coremark,memory_mb,disk_mb
	
	info["weight"] = str(coremark) + " " + str(memory_mb) + " " + str(disk_mb)
	pub_nw = device_networks[gw]["public"]
    	pvt_nw = device_networks[gw]["private"]
	#print pub_nw,pvt_nw
	i = all_devices_list.index(gw)
	for p in pub_nw:
   	    conn_dev = []
   	    bw = public_networks[p]["bandwidth_mbps"]
    	    conn_dev = public_networks[p]["devices"]
            for c in conn_dev:
            	index = str(all_devices_list.index(c)+1)
                if index == str(i+1):
                    continue
            	connections[index] = bw

    	for p in pvt_nw:
    	    conn_dev = []
    	    bw = private_networks[p]["bandwidth_mbps"]
    	    conn_dev = private_networks[p]["devices"]
    	    for c in conn_dev:
		if c in all_devices_list:
		    if index == str(i+1):
                    	continue
    	            index = str(all_devices_list.index(c)+1)
    	            connections[index] = bw
    	info["connections"] = connections
	#meta_name = "meta-{0}".format(meta_index)
	#all_devices_list.append(meta_name)
	#print all_devices_list.index(gw)
	metis_input[str(all_devices_list.index(gw)+1)] = info
	#meta_index += 1
	#print metis_input



#print all_devices_list

for i in range(len(all_devices_list)):
    device = all_devices_list[i]
    if device not in meta_devices:
	info = {}
	networks = []
	connections = {}

    	device_type = infra_config["devices"][device]["device_type"]
    	coremark = device_types[device_type]["coremark"]
    	memory_mb = device_types[device_type]["memory_mb"]
    	disk_mb = device_types[device_type]["disk_mb"]
    	info["weight"] = coremark + " " + memory_mb + " " + disk_mb


    	pub_nw = device_networks[device]["public"]
    	pvt_nw = device_networks[device]["private"]
	#print device,pvt_nw
    	for p in pub_nw:
    	    conn_dev = []
    	    bw = public_networks[p]["bandwidth_mbps"]
   	    conn_dev = public_networks[p]["devices"]
            for c in conn_dev:
                index = str(all_devices_list.index(c)+1)
            	if index == str(i+1):
                    continue
                connections[index] = bw

    	for p in pvt_nw:
    	    conn_dev = []
    	    bw = private_networks[p]["bandwidth_mbps"]
    	    conn_dev = private_networks[p]["devices"]
	    gw = private_networks[p]["gateway"]
	    conn_dev.append(gw)
    	    for c in conn_dev:
		index = str(all_devices_list.index(c)+1)
		if index == str(i+1):
	            continue
    	        connections[index] = bw
	    conn_dev.remove(gw)
    	info["connections"] = connections
    	metis_input[str(all_devices_list.index(device)+1)] = info
print
print "metis_input"
print "path: dump/metis/metis_input"
print
print metis_input   

f = open("dump/metis/metis_input","w")

for m in meta_vertex:
    private_networks.pop(m)
#print private_networks
graph_edges = 0
for p in private_networks:
    n = len(private_networks[p]["devices"])
    n += 1 # for gw device
    graph_edges += (n*(n-1)/2)

for p in public_networks:
    n = len(public_networks[p]["devices"])
    graph_edges += (n*(n-1)/2)

f.write("{0} {1} 011 3\n".format(len(all_devices_list), graph_edges))
for i in range(len(all_devices_list)):
    index = i+1
    m = metis_input[str(index)]
    vertex_weight = m["weight"]
    connections = m["connections"].keys()
    string = str(vertex_weight)
    for c in connections:
        string += (" "+str(c))
        string += ((" ")+str(m["connections"][c]))
    string += "\n"
    f.write(string)
f.close()

with open('dump/infra/updated_devices_list.json','w') as fd:
    fd.write(json.dumps(all_devices_list))

#with open('dump/infra/meta_devices.json','w') as fd:
#    fd.write(json.dumps(meta_devices))

with open('dump/infra/meta_vertex.json', 'w') as file:
     file.write(json.dumps(meta_vertex))

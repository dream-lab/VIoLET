import json

device_networks = {}
public_networks = {}
private_networks = {}
metis_input = {}
infra_config = json.load(open('config/infra_config.json'))
all_devices_list= json.load(open('dump/infra/all_devices_list.json'))
device_types = json.load(open('config/device_types.json'))

edge_count = len(infra_config["devices"]["Edge"].keys())
fog_count = len(infra_config["devices"]["Fog"].keys())

for d in all_devices_list:
    device_networks[d] = {}
    device_networks[d]["private"] = []
    device_networks[d]["public"] = []

private_networks = infra_config["private_networks"]
for p in private_networks:
    gw = private_networks[p]["gw"]
    device_networks[gw]["private"].append(p)
    conn_dev = private_networks[p]["conn_dev"]
    for d in conn_dev:
        device_networks[d]["private"].append(p)

public_networks = infra_config["public_networks"]
for p in public_networks:
    conn_dev = public_networks[p]["conn_dev"]
    for d in conn_dev:
        device_networks[d]["public"].append(p)

for i in range(len(all_devices_list)):
    info = {}
    networks = []
    connections = {}
    device = all_devices_list[i]
    if(i < fog_count):
        device_type = infra_config["devices"]["Fog"][device]["device_type"]
        info["weight"] = device_types["fog_device_types"][device_type]["coremark"]
    else:
        device_type = infra_config["devices"]["Edge"][device]["device_type"]
        info["weight"] = device_types["edge_device_types"][device_type]["coremark"]

    pub_nw = device_networks[device]["public"]
    pvt_nw = device_networks[device]["private"]

    for p in pub_nw:
        conn_dev = []
        bw = public_networks[p]["bw"]
        conn_dev = public_networks[p]["conn_dev"]
        for c in conn_dev:
            index = str(all_devices_list.index(c)+1)
            if index == str(i+1):
                continue
            connections[index] = bw

    for p in pvt_nw:
        conn_dev = []
        bw = private_networks[p]["bw"]
        conn_dev = private_networks[p]["conn_dev"]
        for c in conn_dev:
            index = str(all_devices_list.index(c)+1)
            connections[index] = bw
    info["connections"] = connections
    metis_input[str(all_devices_list.index(device)+1)] = info


f = open("dump/metis/metis_input","w")

graph_edges = 0
for p in private_networks:
    n = len(private_networks[p]["conn_dev"])
    n += 1 # for gw device
    graph_edges += (n*(n-1)/2)

for p in public_networks:
    n = len(public_networks[p]["conn_dev"])
    graph_edges += (n*(n-1)/2)

f.write("{0} {1} 011\n".format(edge_count+fog_count, graph_edges))
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

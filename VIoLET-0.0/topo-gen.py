import json
import random

n = input("number of device?\n")
m = input("number of gateway devices?\n")
#Ed = input("Edge density(%) for public network?\n")

print "Creating a network topology"

#Prepare device array
fog = "Fog-"
edge = "Edge-"

devices=[]
fog_device=[]
edge_device=[]

for i in range (1,m+1):
    f = "Fog-{0}".format(i)
    fog_device.append(f)
    devices.append(f)

num_pvt_networks = m

num_edge_devices = n-m

num_edge_per_network = (num_edge_devices/num_pvt_networks)

remanant = num_edge_devices % num_pvt_networks

for i in range(1,num_pvt_networks+1):
    if(i == num_pvt_networks and remanant != 0):
        num_edge_per_network += remanant
    for j in range(1,num_edge_per_network+1):
        e = "Edge-{0}.{1}".format(i,j)
        edge_device.append(e)
        devices.append(e)
print devices

with open('dump/topo-devices', 'w') as fd:
     fd.write(json.dumps(devices))
with open('dump/topo-edge-devices', 'w') as fd:
     fd.write(json.dumps(edge_device))
with open('dump/topo-fog-devices', 'w') as fd:
     fd.write(json.dumps(fog_device))



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
    pvt = "cibo-private-{0}".format(i)
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
print "\nPrivate network\n"
print private_networks_dict

with open('dump/topo-pvt', 'w') as fd:
     fd.write(json.dumps(private_networks_dict))


num_edge_per_network = (num_edge_devices/num_pvt_networks)


#Create public networks
public_networks_dict = {}
BW = ["25","50","125","250"]
LATENCY = ["5","20","50","100"]
p = {}
conn_dev = []
pub = "cibo-public-{0}".format(1)
bw = BW[random.randint(0,3)]
latency = LATENCY[random.randint(0,3)]
conn_dev = fog_device
p["bw"] = bw
p["latency"] = latency
p["conn_dev"] = conn_dev
public_networks_dict[pub] = p

print "\nPublic network\n"
print public_networks_dict

with open('dump/topo-pub', 'w') as fd:
     fd.write(json.dumps(public_networks_dict))


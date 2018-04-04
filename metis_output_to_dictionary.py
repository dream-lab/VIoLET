import json
import sys

infra_config = json.load(open("config/infra_config.json"))
edge_count = len(infra_config["devices"]["Edge"])
fog_count = len(infra_config["devices"]["Fog"])

file_name = sys.argv[1]
with open(file_name) as f:
    content = f.readlines()
content = [x.strip("\n") for x in content]

num_devices = edge_count + fog_count
num_fog = fog_count
num_edge = num_devices - num_fog
num_edge_per_network = int(num_edge / num_fog)

partitions = {}
fog = {}
edge = {}

#Get Partition for Fog
for i in range(0,num_fog):
    partitions["Fog-{0}".format(i+1)] = content[i]

k = num_fog
for i in range(1, num_fog+1):
    for j in range(1, num_edge_per_network+1):
        partitions["Edge-{0}.{1}".format(i,j)] = content[k]
        k += 1

with open('dump/metis/metis_partitions', 'w') as file:
    file.write(json.dumps(partitions))

print partitions

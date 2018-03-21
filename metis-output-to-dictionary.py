import json
import sys
import pprintpp
#devices = json.load(open('metis-input.part.2'))

with open("metis-input.part.10") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip("\n") for x in content]
num_devices = 408
num_fog = 8
num_edge = num_devices - num_fog
num_edge_per_network = int(num_edge / num_fog)

partitions = {}
fog = {}
edge = {}

#Get Partition for Fog
for i in range(0,num_fog):
    partitions["Fog-{0}".format(i+1)] = content[i]

#partitions["Fog"] = fog

k = num_fog
for i in range(1, num_fog+1):
    for j in range(1, num_edge_per_network+1):
        partitions["Edge-{0}.{1}".format(i,j)] = content[k]
        k += 1
#partitions["Edge"] = edge

with open('algo-partitions', 'w') as file:
    file.write(json.dumps(partitions))

print partitions
pprintpp.pprint(partitions)

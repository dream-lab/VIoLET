import json
import sys

infra_config = json.load(open("config/infra_config.json"))
all_devices_list = json.load(open("dump/infra/all_devices_list.json"))
vm_config = json.load(open("config/vm_config.json"))
device_types = json.load(open("config/device_types.json"))
vm_types = json.load(open("config/vm_types.json"))

edge_count = 0 #len(infra_config["devices"]["Edge"])
fog_count = 0 #len(infra_config["devices"]["Fog"])

for device in all_devices_list:
    if "Edge" in device:
        edge_count+=1
    else:
        fog_count+=1

print edge_count, fog_count

file_name = sys.argv[1]
number_of_vms = int(sys.argv[2])

with open(file_name) as f:
    content = f.readlines()
content = [x.strip("\n") for x in content]

num_devices = edge_count + fog_count
num_fog = fog_count
num_edge = num_devices - num_fog
num_edge_per_network = int(num_edge / num_fog)

container_vm = vm_config["container_VM"]
container_vm_names = container_vm.keys()

container_vm_coremark = []

for c in container_vm:
    container_vm_coremark.append(int(vm_types[container_vm[c]["vm_type"]]["coremark"]))
print container_vm_coremark
vm_coremark_metis = [0] * number_of_vms


i = 0
for d in all_devices_list:
    #if i < num_fog:
    #    device = "Fog"
    #    device_type = "fog_device_types"
    #else:
    #    device = "Edge"
    #    device_type = "edge_device_types"
    dt = infra_config["devices"][d]["device_type"]
    c = device_types[dt]["coremark"]
    vm_coremark_metis[int(content[i])] += int(c)
    i += 1

print vm_coremark_metis

i = 0
for vm_c in vm_coremark_metis:
    if vm_c > container_vm_coremark[i]:
        print "Metis partitions improper. Rerun the gpmetis command"
        sys.exit(0)
    i += 1

partitions = {}
i = 0
for d in all_devices_list:
    partitions[d] = content[i]
    i += 1

with open('dump/metis/metis_partitions.json','w') as file:
    file.write(json.dumps(partitions))

print "Metis partitions for container distribution is properly generated"

print partitions

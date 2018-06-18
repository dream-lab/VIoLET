import json
import sys

infra_config = json.load(open("config/infra_config.json"))
all_devices_list = json.load(open("dump/infra/all_devices_list.json"))
vm_config = json.load(open("config/vm_config.json"))
device_types = json.load(open("config/device_types.json"))


edge_count = len(infra_config["devices"]["Edge"])
fog_count = len(infra_config["devices"]["Fog"])

file_name = sys.argv[1]
number_of_vms = int(sys.argv[2])

with open(file_name) as f:
    content = f.readlines()
content = [x.strip("\n") for x in content]

num_devices = edge_count + fog_count
num_fog = fog_count
num_edge = num_devices - num_fog
num_edge_per_network = int(num_edge / num_fog)

container_vm = vm_config["container_host_VM"]
container_vm_names = container_vm.keys()

container_vm_coremark = []

for c in container_vm_names:
    container_vm_coremark.append(int(container_vm[c]["coremark"]))
print container_vm_coremark

vm_coremark_metis = [0] * number_of_vms


i = 0
for d in all_devices_list:
    if i < num_fog:
        device = "Fog"
        device_type = "fog_device_types"
    else:
        device = "Edge"
        device_type = "edge_device_types"
    dt = infra_config["devices"][device][d]["device_type"]
    c = device_types[device_type][dt]["coremark"]
    vm_coremark_metis[int(content[i])] += int(c)
    i += 1

print vm_coremark_metis

partitions = {}
i = 0
for d in all_devices_list:
    partitions[d] = content[i]
    i += 1

with open('dump/metis/metis_partitions.json','w') as file:
    file.write(json.dumps(partitions))


i = 0
for vm_c in vm_coremark_metis:
    if vm_c > container_vm_coremark[i]:
        print "Metis partitions improper. Rerun the gpmetis command"
        sys.exit(0)
    i += 1

print "Metis partitions for container distribution is properly generated"



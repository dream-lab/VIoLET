import json
import sys

infra_config = json.load(open("config/infra_config.json"))
#all_devices_list = json.load(open("dump/infra/all_devices_list.json"))
updated_devices_list = json.load(open("dump/infra/updated_devices_list.json"))
vm_config = json.load(open("config/vm_config.json"))
device_types = json.load(open("config/device_types.json"))
vm_types = json.load(open("config/vm_types.json"))

edge_count = 0 #len(infra_config["devices"]["Edge"])
fog_count = 0 #len(infra_config["devices"]["Fog"])


for device in updated_devices_list:
    if "Edge" in device:
        edge_count+=1
    else:
        fog_count+=1

#print edge_count, fog_count

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

print "Considering all VMs are same and similar latency across all the VMs"
vm_type = container_vm[container_vm_names[0]]["vm_type"]
print vm_type
print

container_vm_coremark = []
container_vm_memory_mb = []
container_vm_disk_mb = []
for c in container_vm:
    container_vm_coremark.append(int(vm_types[container_vm[c]["vm_type"]]["coremark"]))
    container_vm_memory_mb.append(int(vm_types[container_vm[c]["vm_type"]]["memory_mb"]))
    container_vm_disk_mb.append(int(vm_types[container_vm[c]["vm_type"]]["disk_mb"]))
print container_vm_coremark, container_vm_memory_mb, container_vm_disk_mb

vm_coremark_metis = [0] * number_of_vms
vm_memory_metis = [0] * number_of_vms
vm_disk_metis = [0] * number_of_vms

i = 0
for d in updated_devices_list:
    dt = infra_config["devices"][d]["device_type"]
    c = device_types[dt]["coremark"]
    m_mb = device_types[dt]["memory_mb"]
    d_mb = device_types[dt]["disk_mb"]
    vm_coremark_metis[int(content[i])] += int(c)
    vm_memory_metis[int(content[i])] += int(m_mb)
    vm_disk_metis[int(content[i])] += int(d_mb)
    i += 1

print vm_coremark_metis, vm_memory_metis, vm_disk_metis

i = 0
for vm_c,vm_m,vm_d in zip(vm_coremark_metis,vm_memory_metis,vm_disk_metis):
    if vm_c > container_vm_coremark[i] or vm_m > container_vm_memory_mb[i] or vm_d > container_vm_disk_mb[i]:
        print "Metis partitions improper. Rerun the gpmetis command"
        sys.exit(0)
    i += 1

print "Metis partitions for container distribution is properly generated"

partitions = {}
i = 0
for d in updated_devices_list:
    partitions[d] = content[i]
    i += 1

private_networks = infra_config["private_networks"]
for p in private_networks:
    latency = private_networks[p]["latency_ms"]
    out_latency_ms = vm_types[vm_type]["out_latency_ms"]
    if latency < out_latency_ms:
        meta_vertex = json.load(open("dump/infra/meta_vertex.json"))
	for mv in meta_vertex:
	    gw = meta_vertex[mv]["gateway"]
	    conn_dev = meta_vertex[mv]["devices"]
	    for d in conn_dev:
		partitions[d] = partitions[gw]

with open('dump/metis/metis_partitions.json','w') as file:
    file.write(json.dumps(partitions))

print partitions

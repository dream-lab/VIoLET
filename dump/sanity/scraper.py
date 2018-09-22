import os
import paramiko
import random
import time
import json
import sys
from datetime import datetime
from threading import Thread

startTime = datetime.now()

metis_partitions = json.load(open("../metis/metis_partitions.json","r"))
device_types = json.load(open("../../config/device_types.json","r"))
vm_types = json.load(open("../../config/vm_types.json","r"))
infra_config = json.load(open("../../config/infra_config.json","r"))
devices = infra_config["devices"]
private_networks = infra_config["private_networks"]
public_networks = infra_config["public_networks"]

vm_config = json.load(open("../../config/vm_config.json"))
vm_names = vm_config["container_VM"].keys()
vm_names.sort()


sanity = {}

latency_delta = open("latency_delta","w")
lat = open("latency","w")
for i in range(1,len(sys.argv)):
    sanity[i] = json.load(open(sys.argv[i])) #sys.argv[i]

#print sanity
print "latency"
print
sanity_i = {}

for i in sanity:
    sanity_i = sanity[i]
    for j in sanity_i["latency_numbers"]:
        latency = sanity_i["latency_numbers"][j]
	lat.write(str(float(latency["observed_latency_ms"])/2)+"\n")
        if(latency["observed_latency_ms"]):
            diff = float(latency["observed_latency_ms"]) - (2*float(sanity_i["expected_latency_ms"]))
            per = diff / (2*float(sanity_i["expected_latency_ms"])) * 100
            print per
            latency_delta.write(str(per)+"\n")
latency_delta.close()
lat.close()


bandwidth_delta = open("bandwidth_delta","w")
bandwidth = open("bandwidth","w")
print
print "bandwidth"
print

sanity_i = {}
for i in sanity:
    sanity_i = sanity[i]
    for j in sanity_i["bandwidth_numbers"]:
        bw = sanity_i["bandwidth_numbers"][j]
	bandwidth.write(bw["observed_bandwidth_mbps"]+"\n")
        if(bw["observed_bandwidth_mbps"]):
            diff = float(bw["observed_bandwidth_mbps"]) - float(sanity_i["expected_bandwidth_mbps"])
            per = diff/(float(sanity_i["expected_bandwidth_mbps"])) * 100
            print per
            bandwidth_delta.write(str(per)+"\n")
bandwidth_delta.close()
bandwidth.close()

dev_lat = {}
dev_lat_delta = {}


for d in metis_partitions:
	for p in private_networks:
                if d in private_networks[p]["devices"]:
			dev_lat[d] = private_networks[p]["latency_ms"]
			dev_lat_delta[d] = 0.0

print "********************"
print "device_1","device_2","expected_latency_ms", "observed_latency_ms", "percentage"

		
for i in sanity:
	sanity_i = sanity[i]
    	for j in sanity_i["latency_numbers"]:
        	latency = sanity_i["latency_numbers"][j]
		if(latency["observed_latency_ms"]):
			diff = float(latency["observed_latency_ms"]) - (2*float(sanity_i["expected_latency_ms"]))
            		per = diff / (2*float(sanity_i["expected_latency_ms"])) * 100
			dev_lat[latency["device_1"]] = float(latency["observed_latency_ms"])/2
			dev_lat[latency["device_2"]] = float(latency["observed_latency_ms"])/2
			dev_lat_delta[latency["device_1"]] = per
	                dev_lat_delta[latency["device_2"]] = per
			print latency["device_1"] + "," + latency["device_2"] + "," + str(sanity_i["expected_latency_ms"]) + "," + str(float(latency["observed_latency_ms"])/2) + "," + str(per)

print "**********************"

print dev_lat

vm_nw = {}

for vm in vm_names:
	vm_nw[vm] = set()

for d in metis_partitions:
	for p in private_networks:
		if d in private_networks[p]["devices"]:
			vm_nw[vm_names[int(metis_partitions[d])]].add(p)
	for p in public_networks:
		if d in public_networks[p]["devices"]:
                        vm_nw[vm_names[int(metis_partitions[d])]].add(p)
			
print vm_nw



nw_vm_count = {}
for p in private_networks:
	nw_vm_count[p] = 0

for p in public_networks:
	nw_vm_count[p] = 0


for v in vm_nw:
	for p in vm_nw[v]:
		nw_vm_count[p] += 1

print nw_vm_count

dev_vm_count = {}

for d in metis_partitions:
        for p in private_networks:
                if d in private_networks[p]["devices"]:
                        dev_vm_count[d] = ((dev_lat[d],dev_lat_delta[d]),nw_vm_count[p])
        for p in public_networks:
                if d in public_networks[p]["devices"]:
                        dev_vm_count[d] = ((dev_lat[d],dev_lat_delta[d]),nw_vm_count[p])

print dev_vm_count
print len(dev_vm_count)

lat_vm_count_list = []
lat_delta_vm_count_list = []

lat_vm_count = open("lat_vm_count","w")
lat_delta_vm_count = open("lat_delta_vm_count","w")
for d in metis_partitions:
	lat_vm_count.write(str(dev_vm_count[d][0][0])+","+str(dev_vm_count[d][1])+"\n")
	lat_delta_vm_count.write(str(dev_vm_count[d][0][1])+","+str(dev_vm_count[d][1])+"\n")


#for l in lat_vm_count_list:
#	lat_vm_count.write(str(l)+"\n")
#
#for l in lat_delta_vm_count_list:
#	lat_delta_vm_count.write(str(l)+"\n")

#with open("lat_vm_count",'w') as file:
#    file.write(json.dumps(lat_vm_count_list))
#
#with open("lat_delta_vm_count",'w') as file:
#    file.write(json.dumps(lat_delta_vm_count_list))


lat_vm_count.close()
lat_delta_vm_count.close()





dev_bw = {}
dev_bw_delta = {}
dev_bw_expected = {}

for d in metis_partitions:
        for p in private_networks:
                if d in private_networks[p]["devices"]:
                        dev_bw[d] = private_networks[p]["bandwidth_mbps"]
                        dev_bw_delta[d] = 0.0

	for p in public_networks:
                if d in public_networks[p]["devices"]:
                        dev_bw[d] = public_networks[p]["bandwidth_mbps"]
                        dev_bw_delta[d] = 0.0


print "********************"
print "device_1","device_2","expected_bandwidth_mbps", "observed_bandwidth_mbps", "percentage"
for i in sanity:
        sanity_i = sanity[i]
        for j in sanity_i["bandwidth_numbers"]:
                bw = sanity_i["bandwidth_numbers"][j]
                if(bw["observed_bandwidth_mbps"]):
                        diff = float(bw["observed_bandwidth_mbps"]) - (float(sanity_i["expected_bandwidth_mbps"]))
                        per = diff / (float(sanity_i["expected_bandwidth_mbps"])) * 100
                        dev_bw[bw["device_1"]] = float(bw["observed_bandwidth_mbps"])
                        dev_bw[bw["device_2"]] = float(bw["observed_bandwidth_mbps"])
                        dev_bw_delta[bw["device_1"]] = per
                        dev_bw_delta[bw["device_2"]] = per
			print bw["device_1"] + "," + bw["device_2"] + "," + str(sanity_i["expected_bandwidth_mbps"]) + "," + str(bw["observed_bandwidth_mbps"]) + "," + str(per)


print "*********************"

print dev_bw
print dev_bw_delta

dev_vm_count = {}

for d in metis_partitions:
        for p in private_networks:
                if d in private_networks[p]["devices"]:
                        dev_vm_count[d] = ((dev_bw[d],dev_bw_delta[d]),nw_vm_count[p])
        for p in public_networks:
                if d in public_networks[p]["devices"]:
                        dev_vm_count[d] = ((dev_bw[d],dev_bw_delta[d]),nw_vm_count[p])

print dev_vm_count
print len(dev_vm_count)

bw_vm_count_list = []
bw_delta_vm_count_list = []

bw_delta_expected = open("bw_delta_expected","w")
for p in private_networks:
	devices = private_networks[p]["devices"]
	exp_bw = private_networks[p]["bandwidth_mbps"]
	for d in devices:
		bw_delta_expected.write(str(exp_bw) + "," + str(dev_bw_delta[d]) + "\n")

bw_delta_expected.close()


bw_vm_count = open("bw_vm_count","w")
bw_delta_vm_count = open("bw_delta_vm_count","w")
for d in metis_partitions:
        bw_vm_count.write(str(dev_vm_count[d][0][0])+","+str(dev_vm_count[d][1])+"\n")
        bw_delta_vm_count.write(str(dev_vm_count[d][0][1])+","+str(dev_vm_count[d][1])+"\n")


#for l in lat_vm_count_list:
#       lat_vm_count.write(str(l)+"\n")
#
#for l in lat_delta_vm_count_list:
#       lat_delta_vm_count.write(str(l)+"\n")

#with open("lat_vm_count",'w') as file:
#    file.write(json.dumps(lat_vm_count_list))
#
#with open("lat_delta_vm_count",'w') as file:
#    file.write(json.dumps(lat_delta_vm_count_list))


bw_vm_count.close()
bw_delta_vm_count.close()


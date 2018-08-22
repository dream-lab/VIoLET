import json
import matplotlib
matplotlib.use('Agg')
#from matplotlib_venn import venn3, venn3_circles, venn2, venn2_circles
import venn
from matplotlib import pyplot as plt
import numpy as np
import sys

infra_config = json.load(open('config/infra_config.json'))
metis_partitions = json.load(open('dump/metis/metis_partitions.json'))
vm_config = json.load(open('config/vm_config.json'))
private_networks = infra_config['private_networks']
public_networks = infra_config['public_networks']
vm_names = sorted(vm_config['container_VM'])


vm_devices = {}

for vm in vm_names:
	vm_devices[vm] = set()

#print vm_devices

for d in metis_partitions.keys():
	idx = int(metis_partitions[d])
	vm_devices[vm_names[idx]].add(d)

venn_list = []
label_list = []

for vm in vm_names:
        venn_list.append(vm_devices[vm])
        label_list.append(vm)



#plt.figure(figsize=(4,4))
#venn3(venn_list,label_list)

#venn_list = []
#label_list = []


nw_devices = {}

for p in private_networks:
	nw_devices[p] = set()
	gw = private_networks[p]['gateway']
	nw_devices[p].add(gw)
	for d in private_networks[p]['devices']:
		nw_devices[p].add(d)
	venn_list.append(nw_devices[p])
	label_list.append(p)

#labels = venn.get_labels(venn_list)
#print labels

#venn.venn6(labels,names=label_list)


#venn_list = []
#label_list = []


for p in public_networks:
	nw_devices[p] = set()
	gw = public_networks[p]['gateway']
	nw_devices[p].add(gw)
	for d in public_networks[p]['devices']:
		nw_devices[p].add(d)
	venn_list.append(nw_devices[p])
	label_list.append(p)

#venn2(venn_list,label_list)


fig,ax = plt.subplots()


if (len(venn_list) == 2):
	labels = venn.get_labels(venn_list)
	venn.venn2(labels,names=label_list)
elif (len(venn_list) == 3):
        labels = venn.get_labels(venn_list)
        venn.venn3(labels,names=label_list)
elif (len(venn_list) == 4):
        labels = venn.get_labels(venn_list)
        venn.venn4(labels,names=label_list)
elif (len(venn_list) == 5):
        labels = venn.get_labels(venn_list)
        venn.venn5(labels,names=label_list)
elif (len(venn_list) == 6):
        labels = venn.get_labels(venn_list)
        venn.venn6(labels,names=label_list)
else:
	print "dislay venn diagram of first 6 labels"
        labels = venn.get_labels(venn_list[:6])
        venn.venn6(labels,names=label_list)


print
plt.title("Deployment Diagram") 
#ax.set_title("{}".format(sys.argv[1]))
#ax.set_xlabel("Virtual Machines")
#ax.set_ylabel("{}".format(sys.argv[1]))
#plt.legend(loc="best")
#plt.subplots_adjust(right=0.85)

#plt.annotate('Unknown set', xy=v.get_label_by_id('100').get_position() - np.array([0, 0.05]), xytext=(-70,-70),
#             ha='center', textcoords='offset points', bbox=dict(boxstyle='round,pad=0.5', fc='gray', alpha=0.1),
#             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5',color='gray'))
plt.show()

fig = matplotlib.pyplot.gcf()
fig.set_size_inches(15.5, 6.5)

######################################################################
###########            Plot Computation Ends          ################
######################################################################

# Save the figure
fig.savefig(sys.argv[1]+".png", bbox_inches='tight')
print("\n[SUCCESS] : Plot generated Successfully!")
print("[PATH] : " + sys.argv[1]+".png")



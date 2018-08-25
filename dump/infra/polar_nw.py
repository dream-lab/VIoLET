import numpy as np
import matplotlib
matplotlib.use('SVG')
import matplotlib.pyplot as plt 

import sys
import json


infra_config = json.load(open('../../config/infra_config.json'))
metis_partitions = json.load(open('../metis/metis_partitions.json'))
vm_config = json.load(open('../../config/vm_config.json'))
private_networks = infra_config['private_networks']
public_networks = infra_config['public_networks']
vm_names = vm_config['container_VM'].keys()
device_types = json.load(open('../../config/device_types.json'))

devices = json.load(open('deployment_output.json'))

r_devices = {}
theta_devices = {}
size_devices = {}
color_devices = {}

vm_names.insert(0,"M")


for vm in vm_names:
	r_devices[vm] = []
	theta_devices[vm] = []
	size_devices[vm] = []
	color_devices[vm] = []

r_devices['M'] = ['VM']
theta_devices['M'] = [0]	#['violet_private_1','violet_private_2','violet_private_3','violet_public_1']

theta_nw = {
	'violet_private_1':0,	#0,
	'violet_private_2':1.57,	#90,
	'violet_private_3':3.14,	#180,
	'violet_public_1':4.71	#270
}


color_nw = {
        'violet_private_1':"rgb(27,158,119)",
        'violet_private_2':"rgb(217,95,2)",
        'violet_private_3':"rgb(117,112,179)",
        'violet_public_1':"rgb(231,41,138)"
}


size_device_types = {
        'Pi3B':60,
        'Pi3B+':68,
        'TX1':108,
        'Pi2B':44
}



color_device_types = {
        'Pi3B+':'#f195ac',
        'Pi3B':'#c64847',
        'TX1':'#b28bc0',
	'Pi2B':'#00a8ff',
	'SI':'#7fd13b'
}


vm_devices = {
	'M':'',
	'M1':"M1",
	'M2':"M2",
	'M3':"M3"
	}



for d in devices:
	vm = devices[d]['host_vm_name']
	print d, vm
	pub_nw = devices[d]['public_networks']
	pvt_nw = devices[d]['private_networks']
	d_type = infra_config['devices'][d]['device_type']
	if pub_nw:
		r_devices[vm].append(vm_devices[vm])
		nw = pub_nw.keys()[0]
		theta = theta_nw[nw]+0.35
		theta_devices[vm].append(theta)
		theta_nw[nw] = theta
		size_devices[vm].append(size_device_types[d_type])
		color_devices[vm].append(color_device_types[d_type])
	if pvt_nw:
		r_devices[vm].append(vm_devices[vm])	
		nw = pvt_nw.keys()[0]
                theta = theta_nw[nw]+0.18
   		theta_devices[vm].append(theta)
                theta_nw[nw] = theta
		size_devices[vm].append(size_device_types[d_type])
		color_devices[vm].append(color_device_types[d_type])

print r_devices
print theta_devices

fig = plt.figure()
ax = fig.add_subplot(111,polar=True)


for vm in sorted(vm_names):
	plt.scatter(theta_devices[vm],r_devices[vm],color=color_devices[vm],s=size_devices[vm])
	
plt.xticks([0,1.57,3.14,4.71],rotation='vertical',size=20)
plt.yticks(size=20)
#ax.set_xlabel(size=25)
#ax.set_ylabel(size=25)
ax.set_xticklabels(sorted(theta_nw.keys()))
ax.set_theta_direction(-1)
ax.set_theta_zero_location("N")
ax.grid(color='k',linewidth=2)
ax.spines['polar'].set_visible(False)
fig.savefig(sys.argv[1]+".png", bbox_inches='tight')


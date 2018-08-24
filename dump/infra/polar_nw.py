import numpy as np
import matplotlib
matplotlib.use('SVG')
import matplotlib.pyplot as plt 

from plotly.offline.offline import _plot_html

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
	'violet_private_1':0,
	'violet_private_2':90,
	'violet_private_3':180,
	'violet_public_1':270
}


color_nw = {
        'violet_private_1':"rgb(27,158,119)",
        'violet_private_2':"rgb(217,95,2)",
        'violet_private_3':"rgb(117,112,179)",
        'violet_public_1':"rgb(231,41,138)"
}


size_device_types = {
        'Pi3B':15,
        'Pi3B+':17,
        'TX1':27,
        'Pi2B':11
}



color_device_types = {
        'Pi3B+':'#f195ac',
        'Pi3B':'#c64847',
        'TX1':'#b28bc0',
	'Pi2B':'#00a8ff',
	'SI':'#7fd13b'
}



'''
for d in metis_partitions.keys():
	idx = int(metis_partitions[d])
	d_type = infra_config['devices'][d]['device_type']
	r_devices[vm_names[idx]].append(int(device_types[d_type]['coremark']))
'''


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
	#size_devices[vm].append(size_device_types[d_type])
	#color_devices[vm].append(color_device_types[d_type])
	if pub_nw:
		print pub_nw
		r_devices[vm].append(vm_devices[vm])	#r_devices[vm].append(int(device_types[d_type]['coremark']))
		nw = pub_nw.keys()[0]
		theta = theta_nw[nw]+20
		#theta_devices[vm].append(nw)	
		theta_devices[vm].append(theta)
		theta_nw[nw] = theta
		size_devices[vm].append(size_device_types[d_type])
		color_devices[vm].append(color_device_types[d_type])
	if pvt_nw:
		print pvt_nw
		r_devices[vm].append(vm_devices[vm])	#r_devices[vm].append(int(device_types[d_type]['coremark']))
		nw = pvt_nw.keys()[0]
                theta = theta_nw[nw]+10
		print theta
                #theta_devices[vm].append(nw)	
		theta_devices[vm].append(theta)
                theta_nw[nw] = theta
		size_devices[vm].append(size_device_types[d_type])
		color_devices[vm].append(color_device_types[d_type])

print r_devices
print theta_devices


from plotly.offline  import plot
import plotly.plotly as py
import plotly.graph_objs as go




data = []

for vm in vm_names:
	trace = go.Scatterpolargl(
      		r = r_devices[vm],
      		theta = theta_devices[vm],
      		mode = "markers",
      		name = vm,
      		marker = dict(
        		color = color_devices[vm],
        		size = size_devices[vm],
        		line = dict(
        		  color = "black"
        		),
        		opacity = 0.7
      		)
    	)
	data.append(trace)

print data

layout = go.Layout(
    title = "Deployment",
    font = dict(
      size = 30
    ),
    showlegend = False,
    polar = dict(
      bgcolor = "rgb(255, 255, 255)",
      angularaxis = dict(
        tickwidth = 2,
        linewidth = 2,
        layer = "above traces"
      ),
      radialaxis = dict(
        side = "counterclockwise",
        showline = False,
        linewidth = 2,
        tickwidth = 2,
        gridcolor = "black",
        gridwidth = 2
      )
    ),
    paper_bgcolor = "rgb(255, 255, 255)"
)




fig = go.Figure(data=data, layout=layout)
#py.iplot(fig, filename='polar-area-chart')

plot_html = plot({
    "data": data,
    "layout": layout
},filename=sys.argv[1], image_filename=sys.argv[1], image='png', auto_open=True)


#print(plot_html)
#print(sys.argv[1]+".html")



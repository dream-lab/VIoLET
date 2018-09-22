import os
import sys
import json
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt

infra_config = json.load(open("../../config/infra_config.json","r"))
devices = infra_config["devices"]


fig = plt.figure(1)
#Create an Axes Instance
ax = fig.add_subplot(111)
#ax.set_default_color_cycle
plt.grid(which='minor', alpha=0.5)
plt.grid(which='major', alpha=0.5)


f = open(sys.argv[1],'r')
data = f.readlines()
#print data
start_time = data[0].split()[4]
for d in devices:
	#fd = open("device_logs/{}".format(d),"w")
	x = []
	y = []
	for dt in data:
		dev,dtype,vm,cm,start,end = dt.split('\t')
		#print dev,start,cm
		if d == dev:
			print start,start_time
			x.append(float(start) - float(start_time))
			y.append(cm)

	print x
	print y
	plt.plot(x,y)



fig = matplotlib.pyplot.gcf()
fig.set_size_inches(15.5, 6.5)

######################################################################
###########            Plot Computation Ends          ################
######################################################################

# Save the figure
fig.savefig(sys.argv[2], bbox_inches='tight')
print("\n[SUCCESS] : Plot generated Successfully!")
print("[PATH] : " + sys.argv[1])



f.close()


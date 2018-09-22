import pandas as pd
import numpy as np
import matplotlib
import os
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import sys
import os.path
from pylab import *
#import seaborn as sns; sns.set()
import json

infra_config = json.load(open("../../../config/infra_config.json","r"))
devices = infra_config["devices"].keys()

devices_cm = {}

dev_logs = "device_logs"

fig = plt.figure(1)
#Create an Axes Instance
ax = fig.add_subplot(111)
#ax.set_default_color_cycle
plt.grid(which='minor', alpha=0.5)
plt.grid(which='major', alpha=0.5)

for d in devices:
	df = pd.read_csv("{0}/{1}.csv".format(dev_logs,d))
	y = list(df[df.columns[2]])
	x = list(df[df.columns[3]])
	print d
	print x
	print y
	print 
	#ax = sns.lineplot(x,y)
	plt.plot(x,y)
#ax.set_xticklabels(x,size=7,rotation='vertical')

fig = matplotlib.pyplot.gcf()
fig.set_size_inches(15.5, 6.5)

######################################################################
###########            Plot Computation Ends          ################
######################################################################

# Save the figure
fig.savefig(sys.argv[1], bbox_inches='tight')
print("\n[SUCCESS] : Plot generated Successfully!")
print("[PATH] : " + sys.argv[1])




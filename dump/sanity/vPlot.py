#!/usr/bin/python

import pandas as pd
import numpy as np
import matplotlib
import os
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import sys
import os.path
from pylab import *

'''
    Usage :

        python vPlot.py Input-File Out-File xAxis-HeaderLabels X-Axis_Title Y-Axis_Title

    xAxis-HeaderLabels should be comma separated values.
'''

f_mean = open("../mean","a")
f_median = open("../median","a")

#Array Declarations
mean=[]
medians=[]
plotMap=[]
xheaderTicks=[]
xheaderLabels=[x.strip() for x in sys.argv[3].split(',')]
xHeaderLabelAngle=0
indexes_to_take=[]
indexes_to_drop=[]
maxArray=[]

#Use below parameter in pandas to ignore columns
#usecols=["date", "loc", "x"]

#Accepts InputFile for processing
inputFile = pd.read_csv(sys.argv[1], engine='python', header=None)

for i in range(0,len(inputFile.columns)):
    plotMap.append(inputFile[i].dropna().tolist())
    xheaderTicks.append(i+1)

#Prints Summary of InputFile
print("\nInput File Summary: \n")
print(inputFile.describe())

#Creates Figure Instance
plt.ticklabel_format(useOffset=False)
plt.ticklabel_format(style='plain')
plt.grid(which='minor', alpha=0.5)
plt.grid(which='major', alpha=0.5)
fig = plt.figure(1, figsize=(9, 6))

#Create an Axes Instance
ax = fig.add_subplot(111)

# Create the boxplot
bp = ax.violinplot(plotMap,showmedians=True,showmeans=True,showextrema=True)
bp['cmeans'].set_color('b')
bp['cmedians'].set_color('g')

pltno=1

#Vice-City Color Pallete http://www.color-hex.com/color-palette/45584
for pc in bp['bodies']:
    if(pltno % 8 ==0):
        pc.set_facecolor('#00a8ff')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    elif(pltno % 8 ==1):
        pc.set_facecolor('#0266c8')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    elif(pltno % 8 ==2):
        pc.set_facecolor('#f195ac')
        pc.set_edgecolor('black')
    elif(pltno % 8 ==3):
        pc.set_facecolor('#b28bc0')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    elif(pltno % 8 ==4):
        pc.set_facecolor('#7fd13b')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    elif(pltno % 8 ==5):
        pc.set_facecolor('#c64847')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    elif(pltno % 8 ==6):
        pc.set_facecolor('#005bd3')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    else:
        pc.set_facecolor('#c64847')
        pc.set_edgecolor('black')
        pc.set_alpha(1)
    pltno+=1

#Axis Header
ax.set_xticklabels(xheaderLabels,size=7,rotation=xHeaderLabelAngle)
ax.set_ylabel(sys.argv[4],size=12)
ax.yaxis.grid(which='major', alpha=0.5)
ax.set_xticks(xheaderTicks)
ax.minorticks_on()

######################################################################
###########            Plot Computation Begins          ##############
######################################################################

#Appends Mean and Median for each Column to Array
for i in range(0,len(inputFile.columns)):
    mean.append(sum(inputFile[i].dropna().tolist())/len(inputFile[i].dropna().tolist()))
    medians.append(median(inputFile[i].dropna().tolist()))

#Writing Median values
for i in range(1,len(medians) + 1):
    text(i,medians[i-1],'%.1f' % medians[i-1],horizontalalignment='right',color='red')
    #print "medians[i-1]={0} .1f % medians[i-1]={1}".format(medians[i-1],'%.1f' % medians[i-1])
    f_median.write("{0}\n".format('%.1f' % medians[i-1]))


#Writing Mean values
for i in range(1,len(mean) + 1):
    text(i,mean[i-1],'%.1f' % mean[i-1],horizontalalignment='left',color='purple')
    print "mean[i-1]={0} .1f' % mean[i-1]={1}".format(mean[i-1],'%.1f' % mean[i-1])
    f_mean.write("{0}\n".format('%.1f' % mean[i-1]))

f_mean.close()
f_median.close()

#Marking edian with custom symbol
inds = np.arange(1, len(medians) + 1)
ax.scatter(inds, medians, marker='o', color='white', s=15, zorder=3)


#Graph Annotation
#plt.annotate('', (0,0), (0, -20), xycoords='axes fraction', textcoords='offset points', va='top')

#Appends Quantile Info of Printing
quantile25=[]
quantile75=[]

for i in range(0,len(inputFile.columns)):
    quantile25.append(np.percentile([inputFile[i].dropna().tolist()], [25], axis=1)[0])
    quantile75.append( np.percentile([inputFile[i].dropna().tolist()], [75], axis=1)[0])

inds = np.arange(1, len(medians) + 1)
ax.vlines(inds, quantile25, quantile75, color='k', linestyle='-', lw=5)

fig = matplotlib.pyplot.gcf()
fig.set_size_inches(15.5, 6.5)

######################################################################
###########            Plot Computation Ends          ################
######################################################################

# Save the figure
fig.savefig(sys.argv[2], bbox_inches='tight')
print("\n[SUCCESS] : Plot generated Successfully!")
print("[PATH] : " + sys.argv[2])

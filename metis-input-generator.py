#import numpy as np
import random
from pprint import pprint

n = 408
m = 8

fog=[]
edgelist=[]
c=6

for i in range(1,m+1):
     fog.append(i)
     for j in range((n-m)/m):
         edgelist.append((i,c))
         c+=1

edges = 10381
flag = "011"
metis = {}

for i in range(1,n+1):
	neighbor = []
	for j in edgelist:
		if i == j[0]:neighbor.append(j[1])
		if i == j[1]:neighbor.append(j[0])
	metis[i] = neighbor


def dict_insert(a,b,w,aDict):
	if not a in aDict:
		aDict[a] =[(b,w)]
	else:
		aDict[a].append((b,w))

bw=[25,50,75,125,250]

edgeDict={}

for i in range(1,n+1):
	edgeDict[i] = []


c=0
w=random.choice(bw)
for i in fog:
	for j in fog:
		if i==j:pass
		else:
			for x in edgeDict[j]:
				if i == x[0]:
					w = x[1]
				else:
					w  = random.choice(bw)
			dict_insert(i,j,w,edgeDict)
			c=c+1



for f in fog:
	w=random.choice(bw)
	for n1 in metis[f]:
		dict_insert(f,n1,w,edgeDict)
		dict_insert(n1,f,w,edgeDict)
		c=c+2
		for m in metis[f]:
			if n1 == m:
				pass
			else:
				dict_insert(n1,m,w,edgeDict)
				c=c+1

print c

#pprint(edgeDict)
fog_wt=[26371]
edge_wt=[8910, 13717]

pi2 = 1
pi3 = 1
 #f.write("{0} ".format(random.choice(edge_wt)))
f = open("metis-input","w")
f.write("{0} {1} {2}\n".format(n, edges, flag))
for i in range(1,n+1):
	if i in fog:
		f.write("{0} ".format(random.choice(fog_wt)))
	else:
                if(pi2 < 201):
                    pi2 += 1
                    f.write("{0} ".format(edge_wt[0]))
		else:
                    f.write("{0} ".format(edge_wt[1]))
	for j in edgeDict[i]:
		f.write("{0} {1} ".format(j[0],j[1]))
	f.write("\n")

f.close()





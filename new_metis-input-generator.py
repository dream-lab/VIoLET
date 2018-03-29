import random
import json
import sys
import os
from pprint import pprint
import math

infra_config = json.load(open("config/infra-config.json"))

n = len(infra_config["devices"]["Edge"].keys())
m = len(infra_config["devices"]["Fog"].keys())

public_networks_bw = []
public_networks = infra_config["public_networks"].keys()
public_networks.sort()
for i in range(len(public_networks)):
    public_networks_bw.append(infra_config["public_networks"][public_networks[i]]["bw"])

private_networks_bw = []
private_networks = infra_config["private_networks"].keys()
private_networks.sort()
for i in range(len(private_networks)):
    private_networks_bw.append(infra_config["private_networks"][private_networks[i]]["bw"])


print public_networks_bw
print private_networks_bw

#n = 105
#m = 5

fog=[]
edgelist=[]
c = 6

for i in range(1,m+1):
    fog.append(i)
    for j in range((n-m)/m):
        if c > n: break
        edgelist.append((i,c))
        c+=1
     #edgelist[fog[i]] = edge

edges = 1060
flag = "011"

metis = {}

for i in range(1,n+1):
    neighbor = []
    for j in edgelist:
        if i == j[0]:neighbor.append(j[1])
        if i == j[1]:neighbor.append(j[0])
    metis[i] = neighbor

#pprint(metis)

def dict_insert(a,b,w,aDict):
    if not a in aDict:
        aDict[a] =[(b,w)]
    else:
        aDict[a].append((b,w))

bw=[25]

edgeDict={}

for i in range(1,n+1):
    edgeDict[i] = []


c=0
k=0
w = bw[0]
for i in fog:
    for j in fog:
        if i==j:pass
        else:
            for x in edgeDict[j]:
                if i == x[0]:
                    w = x[1]
                else:
                    print k
                    w = bw[0]

            dict_insert(i,j,w,edgeDict)
            c=c+1
    k=k+1


edge_bw=[25,10,50,25,10]
k=0
for f in fog:
    print k
    w = edge_bw[k]
    k = k+1
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
#fog_wt=[26]
#edge_wt=[13]
wt = [76223,26371,8910,13717]
f1=1
f2=4
e1=50
e2=50
k=0
f = open("metis-input","w")
f.write("{0} {1} {2}\n".format(n, edges, flag))
for i in range(1,n+1):
    if i == f1+1:
        k+=1
    if i == f1+f2+1:
        k+=1
    if i == f1+f2+e1+1:
        k+=1
    if i == n+1:
        k+=1

    f.write("{0} ".format(wt[k]))
    for j in edgeDict[i]:
        f.write("{0} {1} ".format(j[0],j[1]))
    f.write("\n")

f.close()

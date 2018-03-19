# VIoLET ( A Large-scale Virtual Environment for Internet of Things)

VIoLET is a virtual environment for defining and launching large scale IoT deployments within cloud VMs. It offers a declarative model to specify container-based compute resources that match the performance of the native edge, fog and cloud devices. They can be inter-connected by complex topologies on which private/public, bandwidth and latency rules are enforced. Users can launch their custom platforms and applications as well.

### Installation
Clone the repo and place it in all the VMs. Install Docker on all the VMs (including the admin VM) using **docker-install** script. 
Start consul on the admin VM with the following command
```sh
docker run -d -p 8500:8500 -h consul --name consul progrium/consul -server -bootstrap
```
start docker on other VMs using following command
```sh
nohup /usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --cluster-advertise <host VM ip_address>:2375 --cluster-store consul://<address of the machine running consul>:8500 &
```
### Run VIoLET

##### Step 1 - [Generate random topology]
Run topo-gen.py. Input the number of devices and the number of Fog devices / Gateway devices. The remaining devices will be Edge devices and they are equally distributed across the private networks. (number of private networks is equal to the number of Fog devices)
```sh
python topo-gen.py
```

##### Step 2 - [Run Metis and generate partitions]
###### Step 2.1
In the metis-input-generator.py file, modify the number of devices and Fog devices. (Note: these values should be the same as mentioned in previous step) Then run the following command which will generate **metis-input** file
```sh
python metis-input-generator.py
```
###### Step 2.2
You must install Metis in your machine (http://glaros.dtc.umn.edu/gkhome/metis/metis/download)
run the following command. Number of VMs needed for the config is obtained by running coremark and doing the calculations.
```sh
gpmetis metis-input <number_of_VMs>
```
###### Step 2.3
Run metis-output-to-dictionary.py file to convert the metis output file to a python dictionary. Copy paste the output in partitions{} in infra-setup.py file.
```sh
python metis-output-to-dictionary.py
```
##### Step 3 - [Deploy VIoLET]
###### Step 3.1
In infra-setup.py file enter the values for following variables.
```sh
#list out the hostnames of VMs
hosts = [] 

#give the path for the private key to ssh into VM
key_path = "" 

#user name to ssh into VMs
user = ""

#copy paste the metis dictionary output here
partitions = {}

#Based on coremark benchmark calculations enter the cpu ratio of the container wrt to host VMs.
cpus = ""
```
After entering the values. Make sure the topology dictionary(s) is available in **dump** directory.

###### Step 3.2
Run the infra-setup.py file to deploy the containers network bridges and the connectivity.
```sh
python infra-setup.py
```
##### Step 3 - [Sanity check]
Login to any of the VM (except admin VM) to view the network bridges that are created.
```sh
docker network ls
```
Sanity check script needs the network name as an input.
```sh
python sanity.py <network_name>
```
All the numbers are gathered and are made available in **dump** directory.

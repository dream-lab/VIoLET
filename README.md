# VIoLET: A *L*arge-scale *V*irtual *E*nvironment for *I*nternet *o*f *T*hings
ABSTRACT: IoT deployments have been growing manifold, encompassing sensors, networks, edge, fog and cloud resources. Despite the intense interest from researchers and practitioners, most do not have access to large scale IoT testbeds for validation. Simulation environments that allow analytical modeling are a poor substitute for evaluating software platforms or application workloads in realistic computing environments. Here, we propose VIoLET, a virtual environment for defining and launching large scale IoT deployments within cloud VMs. It offers a declarative model to specify container-based compute resources that match the performance of the native edge, fog and cloud devices. They can be inter-connected by complex topologies on which private/public, bandwidth and latency rules are enforced. Users can launch their custom platforms and applications as well. We validate VIoLET for deployments with > 400 devices and > 1500 cores, and show that the virtual IoT environment closely matches the expected compute and network performance at modest costs.

### Clone the Repo
For present version of VIoLET you would need Amazon EC2 instances. One of the VM will act as a admin VM which will deploy VIoLET infrastructure on other VMs (For the current version of VIoLET, VMs must be of same type). Clone the repository and place it on the Admin VM.<br />
Note: Apart from consul (a key store database) No other devices are deployed on the Admin VM. Hence the compute capabilties of the admin VM could be bare minimum. (For ex: a t2.micro EC2 instance will suffice)

### Coremark calculations
This step is needed to determine the number of VMs we will need to deploy the desired config. We can mention the number of devices, their types and network connectivity in the **infra-config.json** file. Create an Amazon VM instance. Download and Install coremark (link - ) on the VM. Follow the instructions to compile and run coremark. Once you get the coremark numbers. Calculate the number of VMs and cpus ratio for each device.<br />
The following example for D105 will explain it better.
<br />
D105 (100 Edge devices, 5 Fog devices)
Amongst 100 Edge devices, let us assume there are 50 Raspberry Pi2B devices and 50 Raspberry Pi3B devices. Similarly let there be 4 Nvidia Jetson Tx1, Fog devices and 1 SoftIron overdrive 3000, Fog device. And let the VM be m5.12xlarge (48 cores)

Going by the D105 configuration, to determine the number of VMs and --cpus, the calculations will be as such.
![Alt text](https://github.com/dream-lab/VIoLET/blob/version-0.1.0/coremark.png)

### Generate infra-config
**infra-config** is the input file for VIoLET. This file contains the device details and network connectivity details to deploy the system. **infra-config-d105.json** is for D105 and **infra-config-d408** is for D408. To use these sample json, rename the file to just **infra-config.json**. User can write their own json with the exact syntax as mentioned in the sample file. Alternatively, for larger deployments user can use **json-gen.py** and provide the inputs as requested by the script.
```sh
python json-gen.py 
```

### Docker Installation
Install Docker on all the VMs (including the admin VM) using **docker-install** script.
```sh
./docker-install
```
Start consul on the admin VM with the following command. Consul is a key-store database to creat docker overlay networks.
```sh
docker run -d -p 8500:8500 -h consul --name consul progrium/consul -server -bootstrap
```
Start docker on other VMs using following command. Make sure you put the right IP addresses as mentioned in the command.
```sh
nohup /usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --cluster-advertise <host VM ip_address>:2375 --cluster-store consul://<address of the machine running consul>:8500 &
```
### Run VIoLET

##### Step 1 - [Run Metis and generate partitions]
###### Step 1.1
In the **metis-input-generator.py** file, modify the number of devices and Fog devices. (Note: these values should be the same as mentioned in previous step) Then run the following command which will generate **metis-input** file
```sh
python metis-input-generator.py
```
###### Step 1.2
You must install Metis in your machine (http://glaros.dtc.umn.edu/gkhome/metis/metis/download)
run the following command.
```sh
gpmetis metis-input <number_of_VMs>
```
###### Step 1.3
Run **metis-output-to-dictionary.py** file to convert the metis output file to a python dictionary. This will generate **algo-partitions.json** file in **dump** directory which will be used by **infra-setup.py** script to distribute the containers across the VMs.
```sh
python metis-output-to-dictionary.py
```
##### Step 2 - [Deploy VIoLET]
###### Step 2.1
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

###### Step 2.2
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

### Publisher-Subscriber Application

The pub-sub model is used as means of data send/receive mechanism by many of the IoT applications. The pub-sub model uses MQTT protocol which comprise of a broker, publisher and subscriber. The subscriber subscribes to a topic hosted by broker. The publisher publishes data to the same topic subscribed by subscriber for the successful data transfer. 
 
In order to perform sanity check of the working of our virtual environment, we designed ping-pong-ping test.
 
The ping-pong-ping test comprise of 2 clients in which both act as publisher and subscriber. The first client will be publishing the data to a topic1 ("pub_" + sensor_id) as well as making an entry in file (same as topic1) and the second client will be subscribing to that topic and will be sending the received messages back to client 1 through a different topic2 ("sub_" + sensor_id) and will be saved to the file (same as topic 2) to perform correctness with the sent data from client 1. The latency is calculated by appending the timestamp with the data sent and subtracting it from the current timestamp on reception at client 1. This is saved to file ("latency_" + sensor_id). The latency data is used to calculate the relative latency percentage to see the latency variation using violin plots.

#### Steps to run the pub-sub application
##### Step 1
After successful run of infra-setup.py and sanity.py, we can start ping-pong-ping test.
##### Step 2
To deploy equal number of publisher and subscriber on edge devices (containers) automatically, run the following command
```sh
python data-gen.py
```
The script will run for around 20 minutes and will collect latency and send/receive of data for 180 entries (data send/receive every second for 180 seconds) on each container under above mentioned files.

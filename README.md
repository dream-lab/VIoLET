# VIoLET: A *L*arge-scale *V*irtual *E*nvironment for *I*nternet *o*f *T*hings

*Shreyas Badiger, Shrey Baheti and Yogesh Simmhan*

*To appear in the 24th International European Conference on Parallel and Distributed Computing (EuroPar), 2018 https://europar2018.org/*

*Selected as a **Distinguished Paper** for presentation at the Plenary Session of EuroPar 2018*

**ABSTRACT:** IoT deployments have been growing manifold, encompassing sensors, networks, edge, fog and cloud resources. Despite the intense interest from researchers and practitioners, most do not have access to large scale IoT testbeds for validation. Simulation environments that allow analytical modeling are a poor substitute for evaluating software platforms or application workloads in realistic computing environments. Here, we propose VIoLET, a virtual environment for defining and launching large scale IoT deployments within cloud VMs. It offers a declarative model to specify container-based compute resources that match the performance of the native edge, fog and cloud devices. They can be inter-connected by complex topologies on which private/public, bandwidth and latency rules are enforced. Users can launch their custom platforms and applications as well. We validate VIoLET for deployments with > 400 devices and > 1500 cores, and show that the virtual IoT environment closely matches the expected compute and network performance at modest costs.

## VIoLET setup
All the VMs must have same centOS version as their operating system (version 7 and above). In VIoLET, one of the VM will act as an admin_VM while the other VMs act as the container_host_VMs. (For the current version of VIoLET, all the container VMs must be of same type).  The architecture diagram below, best explains this setup. VIoLET deploys docker containers as devices. Each of the container's system and network parameters are modified according to the user requirement. Device types, connectivity of the devices and types of sensors for each device are to be entered in **infra_config.json** file. User can add more types of devices or sensors in **device_types.json** and **sensor_types.json** files.<br />
Deploying VIoLET involves 4 parts.

### Part 1 : Generate infra_config.json and calculate the number of container-host-VMs
1. Clone the repository and place it on the admin_VM.
2. Enter the desired infrastructure details in **infra_config.json**. Samples for infra_config is available in VIoLET/config.
3. Decide on the configuration of container_host_VM / Amazon VM instance type and calculate the number of VMs needed to host the desired infra.

### Part 2 : Run Metis and get the container distribution across container_host_VMs.
4. Run metis and generate partitions. This will ensure the containers are optimally distributed across the VMs keeping bandwidth and cpu resources as a constraint.
5. Enter the details pertaining to admin_VM and container_host_VMs (hostname,key path, username etc) in config/vm_config.json file

### Part 3 : Deploy VIoLET
6. Deploy VIoLET using **infra_setup.py** script.

### Part 4 : Run Apps
7. Run sanity check to verify whether bandwidth and latency requirements have met.
8. Run pub_sub application to verify the latency of an application on VIoLET infrastructure.

![Alt text](https://github.com/dream-lab/VIoLET/blob/version-0.1.0/resources/VIoLET-architecture.png)

## Part - 1 [VIoLET Infrastructure & VMs]
### Clone the Repo
To validate VIoLET we have used Amazon EC2 instances. But, there is no dependency on AWS instances as such. One can use any VMs/machines with ssh+key access instead of ssh+password access. <br />
Clone the repository and place it on the Admin VM. <br />
Note: Apart from consul (a key store database) No other devices are deployed on the Admin VM. Hence the compute capabilties of the admin VM could be bare minimum. (For ex: a t2.micro EC2 instance will suffice)


### Generate infra_config.json
**infra_config.json** is the input file for VIoLET. This file contains the device details and network connectivity details to deploy the system. There are few sample config files - **infra_config_d105.json** is for D105 and **infra_config_d408.json** is for D408. To use these sample json, rename the file to **infra_config.json**. Though it is preferred to use **infra_gen.py** to generate the **infra_config.json** file, user can write their own json with the exact syntax as mentioned in the sample file. Use **infra_gen.py** with the following syntax.<br />

<br /> For D105 (100 Edge - {50 Pi2Bs, 50 Pi3Bs}, 5 Fog - {4 TX1, 1 SI}) the command would be as such.
```sh
"""
python infra_gen.py <number_of_devices> <number_of_fog_devices> <number_of_edge_type1,number_of_edge_type2> <number_of_fog_type_1,number_of_fog_type2> <number_of_sensors_per_device> <public_network_edge_density> <container_image>
"""

python infra_gen.py 105 5 50,50 1,4 5 50 centos_systemd
```
At present, the OS image for the containers must either be shrey67/centos_systemd or it can be any docker image which has extended the shrey67/centos_systemd image. Since the image is fetched from the docker hub, the first deployment is expected to take significant amount of time. Alternatively, user can pull the image manually on all the container-host VMs as mentioned in the next few steps.


### Calculating the number of container_host_VMs required
This step is needed to determine the number of container VMs we will need to deploy the infra_config and to compute the --cpus for every container. --cpus is an option given by the docker daemon which specifies the host machine's cpu utilization for a container. <br/>
We mention the number of devices, their types and network connectivity in the **infra_config.json** file. Create the Amazon VM instance. Download and Install coremark (link - https://www.eembc.org/coremark/download.php) on the VM. 
###### Step - 1
After registering and downloading the zipped folder of coremark, cd to the coremark directory and run the following command. 
```sh
make XCFLAGS="-DMULTITHREAD=<number_of_VM_cores> -DUSE_FORK=1" REBUILD=1
```
###### Step - 2
Step 1 generates **coremark.exe**, an executable file. Run the coremark executable.
```sh
./coremark.exe
```
Once you get the coremark numbers (Iterations/Sec). Calculate the number of VMs and cpus ratio for each device.<br />
<br /> <br />
The following example for D105 will explain it better.<br />
D105 (100 Edge devices, 5 Fog devices)
Amongst 100 Edge devices, let us assume there are 50 Raspberry Pi2B devices and 50 Raspberry Pi3B devices. Similarly let there be 4 Nvidia Jetson Tx1, Fog devices and 1 SoftIron overdrive 3000, Fog device. And let the VM be m5.12xlarge (48 cores)

For D105 configuration, to determine the number of VMs and --cpus, the calculations will be as such.
![Alt text](https://github.com/dream-lab/VIoLET/blob/version-0.1.0/resources/coremark.png)

After determining the number of container-host VMs, go ahead and create those many Amazon EC2 instances. All the container host VMs must be of the same type according to the one mentioned in the calculations. VM details are captured in **config/vm_config.json** file. Update the public DNS, key path, user, coremark numbers. Also user must update the --cpus and coremark number for every device type in **config/device_types.json** file. 

### Docker Installation and Image pull
Install Docker on all the VMs (including the admin VM) using **docker_install.sh** script.
```sh
./docker_install.sh
```
Start docker on admin VM with the following command.
```sh
service docker start
```
Start consul on the admin VM with the following command. Consul is a key-store database to creat docker overlay networks.
```sh
docker run -d -p 8500:8500 -h consul --name consul progrium/consul -server -bootstrap
```
Start docker on container-host VMs using following command. Make sure you put the right IP addresses as mentioned in the command.
```sh
nohup /usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --cluster-advertise <host VM ip_address>:2375 --cluster-store consul://<address of the machine running consul>:8500 &
```
Pull the required docker image for VIoLET on all the container-host VMs.
```sh
docker pull shrey67/centos_systemd
```

<br />NOTE: ec2 instances do not come with a disk storage by default. Usually, the ephermal storage drivers aren't sufficent to support the container deployment. User must attach and mount the EBS volume to the container-host VMs and move **/var/lib/docker** to the disk and do a softlink to **/var/lib/docker**. For example, let us assume the disk path to be /disk. Follow these commands after stopping the docker.
```sh
mv /var/lib/docker /disk/docker
ln -s /disk/docker /var/lib/docker
#start the docker daemon as mentioned in the above command.
```
## Part - 2 [Metis Partitions]
### Generate partitions

###### Step 1
Run **metis_input_generator.py** that will generate **dump/metis/metis_input** file
```sh
python metis_input_generator.py
```
###### Step 2
You must install Metis in your machine (http://glaros.dtc.umn.edu/gkhome/metis/metis/download)
run the following command.
```sh
gpmetis dump/metis/metis_input <number_of_VMs>
```
###### Step 3
While partitioning, Metis might over allocate the containers to a container-host VM, since it is making the partitions based on bandwidth. If the **metis_check.py** returns an error asking to re-run the gpmetis, repeat step 2. Otherwise, if the partitioning is correct, this script will generate **metis_partitions.json** file in **dump/metis** directory, which will be used by **infra_setup.py** script to distribute the containers across the VMs. This script takes 2 parameters. metis partition file and the number of VMs.
```sh
python metis_check.py dump/metis/metis_input.part.<number_of_VMs> <number_of_VMs>
```

## Part - 3 [Deploy]
##### Deploy VIoLET
###### Step 1
To deploy VIoLET, make sure the following files are present and updated.
```sh
config/infra_config.json
config/device_types.json
config/sensor_types.json
config/vm_config.json
dump/metis/metis_partitions.json
```
Also ensure docker daemon is started in all the container-host VMs as mentioned earlier.

###### Step 2
Run the **infra_setup.py** to deploy the containers, network bridges and the connectivity.
```sh
python infra_setup.py
```

## Part - 4 [Apps]
#### Sanity check
Sanity check script verfies the following three parameters:
1. Bandwidth - bandwidth is measured by performing **iperf** between two devices in the given network.
2. Latency - latency is measured using **fping** command.
3. Gateway routing - Internet traffic of private network devices are routed through the respective gateway device. This is verified using **traceroute** command.
<br/> To run the sanity check use **sanity.py** which takes network name as the command line arguement.
```sh
docker network ls
```
Login to any of the VM (except admin VM) to view the network bridges that are created. Run the sanity script as mentioned below.
```sh
python sanity.py <network_name>
```
All the numbers are gathered and are made available in **dump/sanity** directory.

#### Publisher-Subscriber Application
VIoLET allows the definition of the virtual sensors that generate data with various distributions within the edge devices (containers). It runs on top of cloud VMs or commodity clusters, allowing it to scale to hundreds or thousands of devices, provided cumulative compute capacity is available. The publisher - subscriber application is used as a means of data trnasfer mechanism by many of the IoT applications. We have developed a basic PUB-SUB applications available under apps folder.
VIoLET provides the ability to simulate the generation odf sensor event streams with various sampling rates and distributions at edge devices for consumption by hosted applications. We have provided the way to initialize the sensors and their various sampling rates and distribution in JSON deployment document. You can also specify the number of sensors of the particular on a edge device to be instantiated. The edge devices are configured based on the deployment document. The virtual sensors, if scpecified, are then started on each device and their streams available on a local port in the device. This is implemented using the python-flask microframework. At this time, the virtual sensors are up and running. After this, the user is provided with the mapping of sensors on each edge devices.
 
In order to perform sanity check of the working of our virtual environment, we designed ping-pong-ping test.
 
The ping-pong-ping test comprise of 2 clients in which both act as publisher and subscriber. The first client will be publishing the data to a topic1 ("pub_" + sensor_id) as well as making an entry in file (same as topic1) and the second client will be subscribing to that topic and will be sending the received messages back to client 1 through a different topic2 ("sub_" + sensor_id) and will be saved to the file (same as topic 2) to perform correctness with the sent data from client 1. The latency is calculated by appending the timestamp with the data sent and subtracting it from the current timestamp on reception at client 1. This is saved to file ("latency_" + sensor_id). The latency data is used to calculate the relative latency percentage to see the latency variation using violin plots.

##### Steps to run the pub-sub application
##### Step 1
After successful run of infra-setup.py and sanity.py, we can start ping-pong-ping test. First change directory to "apps/pub_sub".
##### Step 2
To deploy equal number of publisher and subscriber on edge devices (containers) automatically, run the following command
```sh
python pub_sub.py
```
The script will run for around 10 minutes and will collect latency and send/receive of data for 180 entries (data send/receive every second for 180 seconds) on each container under above mentioned files.

### *ACKNOWLEDGEMENT: This work is supported by grants from VMWARE, Cargill, IUSSTF and IMPRINT*

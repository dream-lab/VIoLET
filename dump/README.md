## Directory - VIoLET/dump

While setting up VIoLET, the scripts generate the json files that are essential for further steps in this directory. 

### VIoLET/dump/metis
This directory will have all the files related to creation of metis_partitions.

### VIoLET/dump/infra
After deploying VIoLET, this directory will have the files with the following information.
1. List of all the devices
2. Device name to Container-host-VM mapping
3. Device names and IP address mapping
and many such files.

### VIoLET/dump/sanity
Once the devices are deployed through VIoLET. It is time to run sanity check to verify the requested system and network parameters have been met. 
This directory will have the files named after the network name which has the bandwidth, latency and routing info.


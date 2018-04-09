## Directory - VIoLET/config

This directory has the config files which are primary input to VIoLET.

### infra_config.json
This json file is the primary input for VIoLET. This file contains following information about the system:
1. Number of Fog and Edge devices
2. Types of the devices (selected from the **device_types.json** file)
3. Number of private and public networks along with the latency and bandwidth parameters for each.
4. Number of sensors per device and their types (selected from the **sensor_types.json** file)

**infra_config.json** file can be generated using **VIoLET/infra_gen.py** script. The guidelines to run this script are stated in **VIoLET/README.md** file.

### device_types.json
This json file consists the types of devices a network can have. The following parameters are required in this file:
1. Name of the device type. (For example - Pi2B, Pi3B etc)
2. coremark value
3. cpus value

Guidelines to calculate (2) and (3) for each device are given in **VIoLET/README.md** file.

### sensor_types.json
This json file the types of sensors a device can support.

### infra_config_d105.json
This is a sample for infra_config.json file with the following:
1. 100 Edge devices (50 - Raspberry Pi2b, 50 - Raspberry Pi3B)
2. 5 Fog devices (4 - Nvidia TX1, 1 - SoftIron Overdrive 3000)

### infra_config_d408.json
This is a sample for infra_config.json file with the following:
1. 400 Edge devices (200 - Raspberry Pi2b, 200 - Raspberry Pi3B)
2. 8 Fog devices (6 - Nvidia TX1, 2 - SoftIron Overdrive 3000)

### infra_config_small.json
This is a sample for infra_config.json file with the following:
1. 4 Edge devices (2 - Raspberry Pi2b, 2 - Raspberry Pi3B)
2. 2 Fog devices (1 - Nvidia TX1, 1 - SoftIron Overdrive 3000)

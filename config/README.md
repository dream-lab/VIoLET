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
This json file consists the types of sensors a device can support. The parameters required in this file are:
1. Name of device type. (For example - Accelerometer, Gyroscope etc)
2. Set id and timestamp to true to append sensor id and timestamp with the values generated based on distribution.
3. Sample size is the number of records to be generated for the sensor data file.
4. Distribution rate and value is used to identify the distribution for timestamp.
5. rate and value params are required for the required paramaters for the distribution rate and value resp.
6. Currently we support 4 types of distribution: Uniform, Gaussian (Normal), Poisson and Custom.
7. For Uniform, set lower_limit and upper_limit.
8. For Normal, set mean and variance.
9. For poisson, set lambda.
10. For custom, provide data files for timestamp and observation values to be used (complete path) for sensor generation.

Note: The file contains the sample configuration of 3 types of sensors. You can add more sensors by appending new json blocks with the required fields (similar to the availabel configuration). 

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

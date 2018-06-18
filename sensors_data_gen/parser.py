import json
import os
from pprint import pprint

data = json.load(open("datagen/infra-config.json"))
sensors = data["sensor_types"]["sensor"]
sensor_types_value = {}

for sensor in sensors:
	sensor_type = str(sensor["type"])
	sensor_id = str(sensor["id"])
	timestamp = str(sensor["timestamp"])
	sample_size = str(sensor["sample_size"])
	dist_rate = str(sensor["dist_rate"])
	dist_value = str(sensor["dist_value"])
	
	if str(sensor["dist_rate"]) == "normal" :
		mean = sensor["rate_params"]["mean"]
		variance = sensor["rate_params"]["variance"]
		rate_params = mean + "," +variance

	if str(sensor["dist_rate"]) == "uniform" :
		lower_limit = sensor["rate_params"]["lower_limit"]
		upper_limit = sensor["rate_params"]["upper_limit"]
		rate_params = lower_limit + "," + upper_limit

	if str(sensor["dist_rate"]) == "poisson" :
		lmbda = sensor["rate_params"]["lambda"]
		rate_params = lmbda

	if str(sensor["dist_rate"]) == "user_defined" :
		path = sensor["rate_params"]["path"]
		rate_params = path

	if str(sensor["dist_value"]) == "normal" :
		mean = sensor["value_params"]["mean"]
		variance = sensor["value_params"]["variance"]
		value_params = mean + "," + variance

	if str(sensor["dist_value"]) == "uniform" :
		lower_limit = sensor["value_params"]["lower_limit"]
		upper_limit = sensor["value_params"]["upper_limit"]
		value_params = lower_limit + "," + upper_limit

	if str(sensor["dist_value"]) == "poisson" :
		lmbda = sensor["value_params"]["lambda"]
		value_params = lmbda

	if str(sensor["dist_value"]) == "user_defined" :
		path = sensor["value_params"]["path"]
		value_params = path
  
	sensor_types_value[sensor_type] =[sensor_id, timestamp, sample_size, dist_rate, rate_params, dist_value, value_params]

edge_sensors = json.load(open("datagen/infra-devices-with-sensors"))

for edge_id in edge_sensors:
	# sensor_id = edge_sensor. #str(device_id) + "_sensor_" + str(sensor["type"]) + "_" + str(sensor_count)
	print(edge_id)
	#sensor_count = sensor_count + 1
	
	for sensor_id in edge_sensors[edge_id]:
		stype = sensor_id.split("_")[1]
		params = sensor_types_value[stype]
		os.system("python datagen/script.py {0} {1} {2} {3} {4} {5} {6} {7}".format(sensor_id,params[0],params[1],params[2],params[3],params[4],params[5],params[6]))

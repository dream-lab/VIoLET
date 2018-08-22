from flask import Flask
import csv
import datetime as dt
import sys

application = Flask(__name__)

sensor_data_dict = {}

count = 0
start_time = dt.datetime.now()

path = "../data"

def response_data(sensor_data,curr_time):
    global count
    count=0
    if len(sensor_data) == 1:
	return sensor_data[count],count
    for data in sensor_data:
        t = dt.datetime.strptime(data.split(",")[1],"%Y-%m-%d %H:%M:%S.%f")
        if t<=curr_time:
            count+=1
        else: break
    return sensor_data[count],count

@application.route("/sensors/<string:sensor>/")
def getMember(sensor):
    global sensor_data_dict
    global count
    curr_time = dt.datetime.now()
    if sensor not in sensor_data_dict:
        f = open(path + "/" + sensor, "r")
        sensor_data_dict[sensor] = f.readlines()
        f.close()

    sensor_data = sensor_data_dict[sensor]
    data,count = response_data(sensor_data,curr_time)
    sensor_data = sensor_data[count:]
    sensor_data_dict[sensor] = sensor_data
    return str(data)

if __name__ == "__main__":
    application.run(host='0.0.0.0')

from flask import Flask
import csv
import datetime as dt
import sys

app = Flask(__name__)


def response_data(sensor_data,curr_time):
    count=0
    for data in sensor_data:
        t = dt.datetime.strptime(data.split(",")[1],"%Y-%m-%d %H:%M:%S.%f")
        if t<=curr_time:
            count+=1
        else: break
    return sensor_data[count],count

@app.route("/sensors/<string:sensor>/")
def getMember(sensor):
    curr_time = dt.datetime.now()
    sensor_data = sensor_data_dict[sensor]
    data,count = response_data(sensor_data,curr_time)
    sensor_data = sensor_data[count:]
    print len(sensor_data)
    sensor_data_dict[sensor] = sensor_data
    return str(data)

if __name__ == "__main__":
    start_time =dt.datetime.now()
    path = sys.argv[2]
    sensors = sys.argv[3]
    sensor_data_dict = {}
    for s in sensors.split(","):
        f = open(path+"/"+s, "r")
        sensor_data_dict[s] = f.readlines()
    app.run(host=sys.argv[1])


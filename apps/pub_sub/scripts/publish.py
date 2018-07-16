import paho.mqtt.client as mqtt
from time import time, sleep
import uuid
import requests
import sys
import os

INTERVAL = 1
QOS = 2

topic1="pub_"
topic2="sub_"
sensor_id = "sensor"

path = "violet/sanity/pub_sub/data"
sub_path = path + "/sub_"
pub_path = path + "/pub_"
lat_path = path + "/latency_"

public_port = 1884
private_port = 1885

pub_data_list = []
sub_data_list = []
cnt = 0

def on_message(client, userdata, message):
    global sub_data_list
    global cnt
    msg = message.payload.decode('utf-8')
    data = str(time()) + "!SubMsgId-" + str(cnt) + "!" + msg
    cnt+=1
    sub_data_list.append(data+"\n")

def main(argv):
    global topic1
    global topic2
    global sensor_id
    global pub_data_list
    sensor_id=argv[1]
    host=argv[2]
    network=argv[5]
    if network=="public":
        port=public_port
    else:
        port=private_port
    topic1 = topic1+sensor_id
    topic2 = topic2+sensor_id
    data_path = argv[3]
    num_msgs = int(sys.argv[4])

    commands = [
		"rm -f {0}/{1}".format(lat_path,sensor_id),
		"rm -f {0}/{1}".format(pub_path,sensor_id),
		"rm -f {0}/{1}".format(sub_path,sensor_id)
	]
    for cmd in commands:
        os.system(cmd)



    client = mqtt.Client()
    client.on_message = on_message
    client.connect(host,port)
    client.subscribe(topic2, qos=QOS)

    client.loop_start()
    for i in range(num_msgs):
        sensor_data = requests.get(data_path).text
        data = "PubMsgId-"+str(i) + "!" + str(time()) + "!" + sensor_data
        client.publish(topic1, data ,qos=QOS)
        pub_data_list.append(data)
        sleep(INTERVAL)
    client.loop_stop()

    f1 = pub_path + sensor_id
    fd1 = open(f1, "w+")
    for d in pub_data_list:
        fd1.write(d)
    fd1.close()
    sleep(5)
    f2 = sub_path + sensor_id
    f3 = lat_path + sensor_id
    fd2 = open(f2, "w+")
    fd3 = open(f3, "w+")
    for d in sub_data_list:
        fd2.write(d)
        sub_time,submsgid,med_time,pubmsgid,pub_time = d.split("!")

        fd3.write(str(float(sub_time)-float(pub_time)) + "\n")
    fd2.close()
    fd3.close()
    client.loop_forever()

if __name__=="__main__":
    main(sys.argv)

import paho.mqtt.client as mqtt
from time import time, sleep
import uuid
import requests
import sys
import os

INTERVAL = 1
QOS = 0

topic1="pub"
topic2="sub"
sensor_id = "sensor"




def on_message(client, userdata, message):
    global sensor_id
    msg = message.payload.decode('utf-8')
    #print(msg)
    f2 = "datagen/sub_" + sensor_id
    fd2 = open(f2,"a+")
    fd2.write(msg+"\n")
    fd2.close()
    t = msg.split("!")
    print("msg: ",t[0])
    #t2 = time()
    #print("current: ",t2)
    rtt = time() - float(t[0])
    f = open("datagen/latency_" + sensor_id,"a+")
    f.write(str(rtt)+"\n")
    f.close()

def main(argv):
    global topic1
    global topic2
    global sensor_id
    sensor_id=argv[1]
    host=argv[2]
    port=1883
    #rtt_array = []
    topic1 = "pub_"+sensor_id
    topic2 = "sub_"+sensor_id
    data_path = "http://127.0.0.1:5000/sensors/" + sensor_id

    commands = [
		"rm -f datagen/latency_{0}".format(sensor_id),
		"rm -f datagen/pub_{0}".format(sensor_id),
		"rm -f datagen/sub_{0}".format(sensor_id)
	]
    for cmd in commands:
        os.system(cmd)
    client = mqtt.Client()
    #client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host,port)
    for i in range(180):
        r=requests.get(data_path)
        data = str(time()) + "!" +r.text
        #t1 = time()
        f1 = "datagen/pub_" + sensor_id
        fd1 = open(f1,"a+")
        fd1.write(data+"\n")
        fd1.close()
        client.loop_start()
        client.publish(topic1, data,qos=QOS)
        #print(topic2)
        sleep(INTERVAL)
        client.subscribe(topic2,1)
        client.loop_stop()
        #t2 = time()
        #print(t2-t1)        
        sleep(INTERVAL)
    client.loop_forever()


if __name__=="__main__":
    main(sys.argv)

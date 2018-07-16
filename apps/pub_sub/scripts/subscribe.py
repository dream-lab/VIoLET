import paho.mqtt.client as mqtt
from time import time, sleep
import uuid
import sys


INTERVAL = 1
QOS = 2
msg="ON"
topic1="pub_"
topic2="sub_"

public_port=1884
private_port=1885


#def on_connect(client, userdata, flags, rc):
#    print("connected")
#    #global topic1
#    #client.subscribe(topic1)
#    #client.publish(topic2, time(), qos=QOS)


def on_message(client, userdata, message):
    global topic2
    global msg
    msg = message.payload.decode('utf-8')
    msgid, pub_time, payload = msg.split("!")
    data = str(time()) + "!" + msgid + "!" + pub_time
    client.publish(topic2, data, qos=QOS)




def main(argv):
    global topic1
    global topic2
    sensor_id=argv[1]
    host=argv[2]
    network=argv[3]
    if network=="public":
        port=public_port
    else:
        port=private_port
    topic1 = topic1+sensor_id
    topic2 = topic2+sensor_id
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(host,port)
    client.subscribe(topic1, qos=QOS)
    client.loop_forever()



if __name__=="__main__":
    main(sys.argv)

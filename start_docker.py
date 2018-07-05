import os
import paramiko
import random
import time
import json
from datetime import datetime
from threading import Thread



startTime = datetime.now()

vm_config = json.load(open("config/vm_config.json"))

admin_ip = vm_config["admin_VM"]["VIoLET_admin"]["hostname_ip"]

container_vm = vm_config["container_VM"]

commands = [
    "service docker start",
    "docker rm -f consul",
    "docker run -d -p 8500:8500 -h consul --name consul progrium/consul -server -bootstrap",
]

for command in commands:
    os.system(command)
    #time.sleep(2)


for c_vm in container_vm:
    host = container_vm[c_vm]["hostname_ip"]
    user = container_vm[c_vm]["user"]
    key = container_vm[c_vm]["key_path"]
    k = paramiko.RSAKey.from_private_key_file(key)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect( hostname = host, username = user, pkey = k)

    command = "nohup sudo /usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock --cluster-advertise {0}:2375 --cluster-store consul://{1}:8500 &".format(host,admin_ip)
    print command
    stdin, stdout, stderr = c.exec_command(command)
    print stdout, stderr
    c.close()





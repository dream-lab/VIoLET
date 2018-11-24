import json
import os
import sys

vm_config = json.load(open("config/vm_config.json"))

container_vm_names = vm_config["container_VM"].keys()

group = "violet"
operation = sys.argv[1]
for vm_name in container_vm_names:
	command = "az vm {0} -g {1} -n {2} &".format(operation,group,vm_name)
	os.system(command)
	


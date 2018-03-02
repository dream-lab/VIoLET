import os
import time

devices = ["F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12","F13","F14","F15","F16","F17","F18","F19","F20"]
for i in devices:
	commands = [
	"sudo docker exec -i {0} python c_dhrystone.py &".format(i),
	"sudo docker exec -i {0} ps aux ".format(i)
	]
	for command in commands:
		print command
		os.system(command)
		time.sleep(0.3)


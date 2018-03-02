import os
import time
import sys
devices = ["F1","F2","F3"] #"F4","F5","F6","F7","F8","F9","F10","F11","F12","F13","F14","F15","F16","F17","F18","F19","F20"]

if (sys.argv[1] == "1"):
	for i in devices:
		command = "sudo docker exec -i {0} python c_coremark_1.py &".format(i)
		os.system(command)
elif(sys.argv[1] == "2"):
	for i in devices:
		command = "sudo docker exec -i {0} python c_coremark_2.py &".format(i)
		os.system(command)
elif(sys.argv[1] == "4"):
	for i in devices:
		command = "sudo docker exec -i {0} python c_coremark_4.py &".format(i)
		os.system(command)


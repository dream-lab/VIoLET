import sys


def main(argv):
    filename = "/etc/mosquitto/mosquitto.conf"    
    f = open(filename,"w")
    data = "bind_address " + argv[1]
    f.write(data)
    f.close()

if __name__ == "__main__":
    main(sys.argv)

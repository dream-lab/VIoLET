import sys

def main(argv):
    if argv[2]=="private":
        filename = "/etc/mosquitto/mosquitto-private.conf"
        f = open(filename,"w")
        data = "bind_address " + argv[1] + "\nlog_type all\nlog_dest file /etc/mosquitto/mosquitto-private.log"  
        f.write(data)
        f.close()
    else:
        filename = "/etc/mosquitto/mosquitto-public.conf"
        f = open(filename,"w")
        data = "bind_address " + argv[1] + "\nlog_type all\nlog_dest file /etc/mosquitto/mosquitto-public.log" 
        f.write(data)
        f.close()

if __name__ == "__main__":
    main(sys.argv)

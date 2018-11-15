import sys
import os

def main(argv):
    if argv[2]=="private":
        filename = "/etc/mosquitto/mosquitto-private.conf"
        f = open(filename,"w")
	log = open("/violet/sanity/pub_sub/mosquitto-private.log","w")
	log.close()
	os.system("chmod o+w /violet/sanity/pub_sub/mosquitto-private.log")
        data = "bind_address " + argv[1] + "\nmax_inflight_messages 1" + "\nlog_type all\nlog_dest file /violet/sanity/pub_sub/mosquitto-private.log" 
        f.write(data)
        f.close()
    else:
        filename = "/etc/mosquitto/mosquitto-public.conf"
        f = open(filename,"w")
	log = open("/violet/sanity/pub_sub/mosquitto-public.log","w")
        log.close()
	os.system("chmod o+w /violet/sanity/pub_sub/mosquitto-public.log")
        data = "bind_address " + argv[1] +"\nmax_inflight_messages 1" + "\nlog_type all\nlog_dest file /violet/sanity/pub_sub/mosquitto-public.log" 
        f.write(data)
        f.close()

if __name__ == "__main__":
    main(sys.argv)

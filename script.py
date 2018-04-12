import numpy as np
import datetime as dt
import sys
import time

#t = ""
#v = ""

#tim=""
#val=""

def main(argv):
	print argv
	filename = argv[1]
	fd = open(filename, "w")

	s_id = bool(argv[2])

	data = ""

	

	timestamp = bool(argv[3]) 

	size = int(argv[4])

	rate = str(argv[5])
	rate_params = argv[6].split(',')

	value = str(argv[7])
	value_params = argv[8].split(',')

	if rate =="user_defined":
		t = open(rate_params[0])
		r_value = t.readlines()
		#print(r_value)
		t.close()

	if value =="user_defined":
		d = open(value_params[0])
		d_value = d.readlines()
		#print d_value
		d.close()


	if s_id:
		data = data + argv[1]
		

	if timestamp:
		st = dt.datetime.now()
	for i in range(size):
		tim=""
		val=""

		

		if rate == "normal":
			r_value = normal(rate_params)
		elif rate == "uniform":
			r_value = uniform(rate_params)
		elif rate == "poisson":
			r_value = poisson(rate_params)
		else: 
			#tim = "time"
			rval = r_value[i].rstrip("\n")
			#print(i)
			#print r_value


		
		if value == "normal":
			d_value = normal(value_params)
		elif value == "uniform":
			d_value = uniform(value_params)
		elif value == "poisson":
			d_value = poisson(value_params)
		else:
			#val = "value"
			dval = d_value[i].rstrip("\n")
			#print d_value
	
		if rate == "user_defined":
			st = rval
		else:
			st = st + dt.timedelta(seconds=abs(r_value))
	
		if value == "user_defined":
			dv = dval
		else:
			dv = d_value

		d = data + "," + str(st) + "," + str(dv) + "\n"
		fd.write(d)
	fd.close()
	#if tim=="time":
	#	t.close()
	#if val=="value":
	#	v.close()


def normal(params):
	return np.random.normal(int(params[0]), int(params[1]))

def uniform(params):
	return np.random.uniform(int(params[0]), int(params[1]))

def poisson(params):
	return np.random.poisson(int(params[0]))


#def custom(f):
#	return f.readline().rstrip('\n')

if __name__ == "__main__":
	main(sys.argv)


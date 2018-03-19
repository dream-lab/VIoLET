import numpy as np
import datetime as dt
import sys
import time


def main(argv):
	print(argv)
	filename = "datagen/" + argv[1]
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

	if value =="user_defined":
		v = open(value_params[0])


	r_value=0
	d_value=0


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
			tim = "time"
			r_value = custom(rate_params, t)


		
		if value == "normal":
			d_value = normal(value_params)
		elif value == "uniform":
			d_value = uniform(value_params)
		elif value == "poisson":
			d_value = poisson(value_params)
		else:
			val = "value"
			d_value = custom(value_params, v)
	
		if rate == "user_defined":
			st = r_value
		else:
			st = st + dt.timedelta(seconds=abs(r_value))
	
		d = data + "," + str(st) + "," + str(d_value) + "\n"
		fd.write(d)
	fd.close()


def normal(params):
	return np.random.normal(int(params[0]), int(params[1]))

def uniform(params):
	return np.random.uniform(int(params[0]), int(params[1]))

def poisson(params):
	return np.random.poisson(int(params[0]))


def custom(params, f):
	return f.readline().rstrip('\n')

if __name__ == "__main__":
	main(sys.argv)

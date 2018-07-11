import numpy as np
import datetime as dt
import sys
import time

time_str = "%Y-%m-%d %H:%M:%S.%f"

sensor_data_path = "violet/sensors/data"
def main(argv):
    print argv
    filename = argv[1]
    fd = open(sensor_data_path + "/" + filename, "w")

    s_id = bool(argv[2])
    data = ""

    timestamp = bool(argv[3])
    duration = int(argv[4])
    rate = str(argv[5])
    rate_params = argv[6].split(',')
    value = str(argv[7])
    value_params = argv[8].split(',')

    if rate =="user_defined":
        t = open(sensor_data_path + "/" + rate_params[0])
        r_val = t.readlines()
        initial_time = dt.datetime.strptime(r_val[0].rstrip(), time_str)
        print initial_time
        #print(r_value)
        t.close()

    if value =="user_defined":
        d = open(sensor_data_path + "/" + value_params[0])
        d_val = d.readlines()
        #print d_value
        d.close()

    if s_id:
        data = data + argv[1]

    if timestamp:
        st = dt.datetime.now()

    i=0
    curr = 0
    while curr < duration:
        tim=""
        val=""
        if rate == "normal":
            r_value = normal(rate_params[0], rate_params[1])
            min_value = float(rate_params[2])
            unit = rate_params[3]
            if unit == "ms":
                min_value /= 1000
                r_value /= 1000
            elif unit == "m":
                min_value *= 60
                r_value *= 60
            elif unit == "h":
                min_value *= 3600
                r_value *= 3600
            else:
                pass
        elif rate == "uniform":
            r_value = uniform(rate_params[0], rate_params[1])
            min_value = float(rate_params[0])
            unit = rate_params[2]
            if unit == "ms":
                min_value /= 1000
                r_value /= 1000
            elif unit == "m":
                min_value *= 60
                r_value *= 60
            elif unit == "h":
                min_value *= 3600
                r_value *= 3600
            else:
                pass
        elif rate == "poisson":
            r_value = poisson(rate_params[0])
            min_value = float(rate_params[1])
            unit = rate_params[2]
            if unit == "ms":
                min_value /= 1000
                r_value /= 1000
            elif unit == "m":
                min_value *= 60
                r_value *= 60
            elif unit == "h":
                min_value *= 3600
                r_value *= 3600
            else:
                pass
        else:
            while (dt.datetime.strptime(r_val[i].rstrip("\n"), time_str) - initial_time).total_seconds() < 0:
                i+= 1
            r_value = (dt.datetime.strptime(r_val[i].rstrip("\n"), time_str) - initial_time).total_seconds()
            #print rval
            i+=1
            min_value = 0
            unit = rate_params[1]
            if unit == "ms":
                r_value /= 1000
            elif unit == "m":
                r_value *= 60
            elif unit == "h":
                r_value *= 3600
            else:
                pass




        if value == "normal":
            d_value = max(float(value_params[2]), normal(value_params[0], value_params[1]))
        elif value == "uniform":
            d_value = uniform(value_params[0], value_params[1])
        elif value == "poisson":
            d_value = max(float(value_params[1]), poisson(value_params[0]))
        else:
            #val = "value"
            d_value = d_val[i].rstrip("\n")
            #print d_value

        curr += max(min_value, r_value)
        if curr > duration:
            break

        st = st + dt.timedelta(seconds=max(min_value, r_value))
        df = data + "," + str(st) + "," + str(d_value) + "\n"

        #print df
        #print dv
        #print st

        fd.write(df)
    fd.close()


def normal(mean, variance):
    return float(np.random.normal(float(mean), float(variance)))

def uniform(lower_limit, upper_limit):
    return float(np.random.uniform(float(lower_limit), float(upper_limit)))

def poisson(lmbda):
    return float(np.random.poisson(float(lmbda)))



if __name__ == "__main__":
    main(sys.argv)


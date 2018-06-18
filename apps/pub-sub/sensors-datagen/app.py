from flask import Flask
import csv
import datetime as dt

app = Flask(__name__)
	
def response_data(name,time_diff):
	filename = "datagen/" + name
	data = ""
	reader = csv.reader(open(filename, "r"))
	d_time = next(reader)
	t = dt.datetime.strptime(d_time[1],"%Y-%m-%d %H:%M:%S.%f")
	count=0
	#reader.seek(count)	
	for row in reader:
		t_row = dt.datetime.strptime(row[1],"%Y-%m-%d %H:%M:%S.%f")
		if (t_row-t)<=time_diff:
			data = row
		else: break
	return data
 
@app.route("/sensors/<string:name>/")
def getMember(name):
	t2 = dt.datetime.now()
	diff = t2-t1
	data = response_data(name,diff)
	return str(data)	
 
if __name__ == "__main__":
	t1 =dt.datetime.now()
	app.run()

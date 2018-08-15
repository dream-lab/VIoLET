from flask import Flask, request
from flask_cors import CORS
import os
import json

app = Flask('violet_ui_backend')
CORS(app)


@app.route('/infra_gen', methods=['GET'])
def infra_gen():
    try:
        os.system("python infra_gen.py ")
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)


@app.route('/metis_gen', methods=['GET'])
def metis_gen():
    try:
        os.system("python metis_input_generator.py ")
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)

@app.route('/partition_gen', methods=['POST'])
def partition_gen():
    try:
        os.system("/usr/local/bin/gpmetis dump/metis/metis_input " + str(request.form['vm']))
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)

@app.route('/metis_check', methods=['POST'])
def metis_check():
    try:
        os.system("python metis_check.py dump/metis/metis_input.part." + str(request.form['vm']) + " " + str(request.form['vm']))
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)

@app.route('/start_docker', methods=['GET'])
def start_docker():
    try:
        os.system("python start_docker.py ")
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)

@app.route('/delete_infra', methods=['GET'])
def delete_infra():
    try:
        os.system("python delete_infra.py ")
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)

@app.route('/infra_setup', methods=['GET'])
def infra_setup():
    try:
        os.system("python infra_setup.py ")
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)

@app.route('/sensor_gen', methods=['GET'])
def sensor_gen():
    try:
        os.system("python sensor_gen.py ")
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)



if __name__ == '__main__':
    app.run()

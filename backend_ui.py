from flask import Flask, request
from flask_cors import CORS
import os
import json

app = Flask('violet_ui_backend')
CORS(app)


@app.route('/infra_gen', methods=['GET'])
def infra_gen():
    try:
        r = os.system("python infra_gen.py ")
        if r != 0:
            raise Exception
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)


@app.route('/metis_gen', methods=['GET'])
def metis_gen():
    try:
        r = os.system("python metis_input_generator.py ")
        if r != 0:
            raise Exception
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)


@app.route('/partition_gen', methods=['POST'])
def partition_gen():
    try:
        r = os.system("/usr/local/bin/gpmetis dump/metis/metis_input " + str(request.form['vm']))
        if r != 0:
            raise Exception
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)


@app.route('/metis_check', methods=['POST'])
def metis_check():
    try:
        r = os.system("python metis_check.py dump/metis/metis_input.part." + str(request.form['vm']) + " " + str(
            request.form['vm']))
        if r != 0:
            raise Exception
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)


@app.route('/start_docker', methods=['GET'])
def start_docker():
    try:
        r = os.system("python start_docker.py ")
        if r != 0:
            raise Exception
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)


@app.route('/delete_infra', methods=['GET'])
def delete_infra():
    try:
        r = os.system("python delete_infra.py ")
        if r != 0:
            raise Exception
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)


@app.route('/infra_setup', methods=['GET'])
def infra_setup():
    try:
        r = os.system("python infra_setup.py ")
        if r != 0:
            raise Exception
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)


@app.route('/sensor_gen', methods=['GET'])
def sensor_gen():
    try:
        r = os.system("python sensor_gen.py ")
        if r != 0:
            raise Exception
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)


if __name__ == '__main__':
    app.run()

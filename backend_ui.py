from flask import Flask, request
from flask_cors import CORS
import os
import json
from subprocess import Popen, PIPE

app = Flask('violet_ui_backend')
CORS(app)


@app.route('/infra_gen', methods=['GET'])
def infra_gen():
    try:
        r, e = Popen(["python", "infra_gen.py", "-s", "10", "-l", "1"], stdout=PIPE, stderr=PIPE).communicate()
        if e != '':
            raise
        return json.dumps({'message': r})
    except:
        return (json.dumps({'message': e}), 500)


@app.route('/infra_gen_input', methods=['GET'])
def infra_gen_input():
    try:
        with open('config/infra_gen.json', 'r') as f:
            d = json.load(f)
            d = json.dumps(d, indent=4)
            return json.dumps({'data': d, 'name': 'infra_gen.json'})
    except:
        return ('Failure', 500)


@app.route('/infra_gen_output', methods=['GET'])
def infra_gen_output():
    try:
        with open('config/infra_config.json', 'r') as f:
            d = json.load(f)
            d = json.dumps(d, indent=4)
            return json.dumps({'data': d, 'name': 'infra_config.json'})
    except:
        return ('Failure', 500)


@app.route('/partition_output', methods=['GET'])
def partition_output():
    try:
        with open('dump/metis/metis_partitions.json', 'r') as f:
            d = json.load(f)
            d = json.dumps(d, indent=4)
            return json.dumps({'data': d, 'name': 'metis_partitions.json'})
    except:
        return ('Failure', 500)


@app.route('/metis_gen', methods=['GET'])
def metis_gen():
    try:
        r, e = Popen(["python", "metis_input_generator.py"], stdout=PIPE, stderr=PIPE).communicate()
        if e != '':
            raise
        return json.dumps({'message': r})
    except:
        return (json.dumps({'message': e}), 500)


@app.route('/partition_gen', methods=['POST'])
def partition_gen():
    try:
        r, e = Popen(["/usr/local/bin/gpmetis", "dump/metis/metis_input", str(request.form['vm'])], stdout=PIPE,
                     stderr=PIPE).communicate()
        if e != '':
            raise
        return json.dumps({'message': r})
    except:
        return (json.dumps({'message': e}), 500)


@app.route('/metis_check', methods=['POST'])
def metis_check():
    try:
        r, e = Popen(["python", "metis_check.py", "dump/metis/metis_input.part." + str(request.form['vm']),
                      str(request.form['vm'])], stdout=PIPE,
                     stderr=PIPE).communicate()
        if e != '':
            raise
        return json.dumps({'message': r})
    except:
        return (json.dumps({'message': e}), 500)


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


@app.route('/sanity_network', methods=['GET'])
def sanity_network():
    try:
        r = os.system("python sanity_network.py ")
        if r != 0:
            raise Exception
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)


@app.route('/sanity_cpu', methods=['GET'])
def sanity_cpu():
    try:
        r = os.system("python sanity_cpu.py ")
        if r != 0:
            raise Exception
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)


@app.route('/pub_sub', methods=['GET'])
def pub_sub():
    try:
        r = os.system("python apps/pub_sub/scripts/pub_sub.py ")
        if r != 0:
            raise Exception
        return json.dumps({'message': 'Success'})
    except:
        return ('Failure', 500)


if __name__ == '__main__':
    app.run()

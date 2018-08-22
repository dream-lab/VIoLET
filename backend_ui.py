from time import sleep

from flask import Flask, request, send_file
from flask_cors import CORS
import os
import json
from subprocess import Popen, PIPE

app = Flask('violet_ui_backend')
CORS(app)


# Infra

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


# Partition

@app.route('/partition_input', methods=['GET'])
def partition_input():
    try:
        d1 = ''
        d2 = ''
        d3 = ''
        with open('config/vm_config.json', 'r') as f:
            d1 = json.load(f)
            d1 = json.dumps(d1, indent=4)
        with open('config/vm_types.json', 'r') as f:
            d2 = json.load(f)
            d2 = json.dumps(d2, indent=4)
        with open('config/device_types.json', 'r') as f:
            d3 = json.load(f)
            d3 = json.dumps(d3, indent=4)
        return json.dumps({'vm_config.json': d1, 'vm_types.json': d2, 'device_types.json': d3})
    except:
        return ('Failure', 500)


@app.route('/partition_output', methods=['GET'])
def partition_output():
    try:
        with open('dump/metis/metis_partitions.json', 'r') as f:
            d = json.load(f)
            d = json.dumps(d, indent=4)
            return json.dumps({'metis_partitions.json': d})
    except:
        return ('Failure', 500)


@app.route('/partition_plot_coremark', methods=['GET'])
def partition_plot_coremark():
    try:
        r, e = Popen(["cd /home/centos/shriram/VIoLET/dump/metis; python bsplot.py coremark"], stderr=PIPE, shell=True).communicate()
        if e != '':
            raise
        return send_file("dump/metis/coremark.png", attachment_filename='coremark.png')
    except:
        return (json.dumps({'message': e}), 500)


@app.route('/partition_plot_memory', methods=['GET'])
def partition_plot_memory():
    try:
        r, e = Popen(["cd /home/centos/shriram/VIoLET/dump/metis; python bsplot.py memory"], stderr=PIPE).communicate()
        if e != '':
            raise
        return send_file("dump/metis/memory.png", attachment_filename='memory.png')
    except:
        return (json.dumps({'message': e}), 500)


@app.route('/partition_plot_disk', methods=['GET'])
def partition_plot_disk():
    try:
        r, e = Popen(["cd /home/centos/shriram/VIoLET/dump/metis; python bsplot.py disk"], stderr=PIPE).communicate()
        if e != '':
            raise
        return send_file("dump/metis/disk.png", attachment_filename='disk.png')
    except:
        return (json.dumps({'message': e}), 500)


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
    # return json.dumps({'message': 'success'})


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
    # return json.dumps({'message': 'success'})


@app.route('/deployment_input', methods=['GET'])
def deployment_input():
    try:
        d1 = ''
        d2 = ''
        with open('config/deployment.json', 'r') as f:
            d1 = json.load(f)
            d1 = json.dumps(d1, indent=4)
        with open('config/sensor_types.json', 'r') as f:
            d2 = json.load(f)
            d2 = json.dumps(d2, indent=4)
        return json.dumps({'deployment.json': d1, 'sensor_types.json': d2})
    except:
        return ('Failure', 500)


@app.route('/deployment_output', methods=['GET'])
def deployment_output():
    try:
        with open('dump/infra/deployment_output.json', 'r') as f:
            d = json.load(f)
            d = json.dumps(d, indent=4)
            return json.dumps({'deployment_output.json': d})
    except:
        return ('Failure', 500)


@app.route('/start_docker', methods=['GET'])
def start_docker():
    try:
        p = Popen(["python", "start_docker.py"])
        sleep(30)
        return json.dumps({'message': "Docker started \n\n"})
    except:
        return (json.dumps({'message': 'Failure'}), 500)


@app.route('/delete_infra', methods=['GET'])
def delete_infra():
    try:
        r, e = Popen(["python", "delete_infra.py"], stderr=PIPE).communicate()
        if e != '':
            raise
        return json.dumps({'message': "Infrastructure deleted \n\n"})
    except:
        return (json.dumps({'message': e}), 500)


@app.route('/infra_setup', methods=['GET'])
def infra_setup():
    try:
        r, e = Popen(["python", "infra_setup.py"], stderr=PIPE).communicate()
        if e != '':
            raise
        return json.dumps({'message': "Infrastructure setup complete \n\n"})
    except:
        return (json.dumps({'message': e}), 500)


@app.route('/sensor_gen', methods=['GET'])
def sensor_gen():
    try:
        r, e = Popen(["python", "sensor_gen.py"], stderr=PIPE).communicate()
        return json.dumps({'message': "Sensor generation complete \n\n"})
    except:
        return (json.dumps({'message': e}), 500)


@app.route('/sanity_network', methods=['GET'])
def sanity_network():
    try:
        p = Popen(["python", "sanity_network.py"])
        sleep(240)
        p = Popen([
                      'cd /home/centos/shriram/VIoLET/dump/sanity; python vPlot.py bandwidth_delta bw.pdf "Bandwidth" "Deviation"'],
                  shell=True)
        p = Popen([
                      'cd /home/centos/shriram/VIoLET/dump/sanity; python vPlot.py bandwidth_delta bw.pdf "Bandwidth" "Deviation"'],
                  shell=True)
        return json.dumps({'message': "CPU sanity check complete \n\n"})
    except:
        return (json.dumps({'message': 'Failure'}), 500)


@app.route('/sanity_cpu', methods=['GET'])
def sanity_cpu():
    try:
        p = Popen(["python sanity_cpu.py 1"], shell=True)
        sleep(240)
        p = Popen(["python sanity_cpu.py 2"], shell=True)
        sleep(60)
        p = Popen([
                      'cd /home/centos/shriram/VIoLET/dump/sanity; python vPlot.py f_pi2b_delta f_pi2b.pdf "Coremark (Pi2B)" "Deviation"'],
                  shell=True)
        p = Popen([
                      'cd /home/centos/shriram/VIoLET/dump/sanity; python vPlot.py f_pi3b_delta f_pi3b.pdf "Coremark (Pi3B)" "Deviation"'],
                  shell=True)
        p = Popen([
                      'cd /home/centos/shriram/VIoLET/dump/sanity; python vPlot.py f_tx1_delta f_tx1.pdf "Coremark (TX1)" "Deviation"'],
                  shell=True)
        p = Popen([
                      'cd /home/centos/shriram/VIoLET/dump/sanity; python vPlot.py f_si_delta f_si.pdf "Coremark (SI)" "Deviation"'],
                  shell=True)
        return json.dumps({'message': "CPU sanity check complete \n\n"})
    except:
        return (json.dumps({'message': 'Failure'}), 500)


@app.route('/pub_sub', methods=['GET'])
def pub_sub():
    try:
        p = Popen(["cd /home/centos/shriram/VIoLET/apps/pubsub; python pub_sub.py"], shell=True)
        sleep(240)
        p = Popen(["cd /home/centos/shriram/VIoLET/apps/pubsub; python sanity.py"], shell=True)
        sleep(90)
        return json.dumps({'message': "Pub/Sub sanity check complete \n\n"})
    except:
        return (json.dumps({'message': 'Failure'}), 500)


if __name__ == '__main__':
    app.run('0.0.0.0')

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
    except Exception as e:
        return (str(e), 500)


@app.route('/metis_gen', methods=['GET'])
def metis_gen():
    try:
        os.system("python metis_input_generator.py ")
        return json.dumps({'message': 'Success'})
    except Exception as e:
        return (str(e), 500)


if __name__ == '__main__':
    app.run()

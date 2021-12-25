import os
import uuid
import requests
from flask import Flask, request, json, jsonify
from keras.models import load_model

from method import Model

model = Model(23 , 224 ,0.0001 ,'../Models/{{ fileName }}.h5')

app = Flask(__name__)
UPLOAD_FOLDER = '../imgs'
redirectPorts ={}
redirectPorts = json.load(open('ip.json'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['img']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4())+ extension
        path = os.path.join(UPLOAD_FOLDER, f_name)
        file.save(path)
        result =int( model.simulation(path)[0])

        port = result + 5001
        levelTwoRequest = requests.post(f'http://{redirectPorts[str(result)]}:{port}', data={'imgPath': path})
        return levelTwoRequest.json()
    else:
        return jsonify(
            status='fail',
            data=None
        )



if __name__ == '__main__':
    app.run(host='{{ip}}' , port={{port}} , debug =True )
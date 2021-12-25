import os
import uuid
import requests
from flask import Flask, request, json, jsonify
from keras.models import load_model

from method import Model

model = Model(23 , 224 ,0.0001 ,'./Models/layer10-wskindiseases.h5')

app = Flask(__name__)
UPLOAD_FOLDER = './imgs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
redirectPorts ={}

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['img']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4())+ extension
        path = os.path.join(app.config['UPLOAD_FOLDER'], f_name)
        file.save(path)
        result =int( model.simulation(path)[0])
        levelTwoRequest= requests.post(f"http://localhost:{redirectPorts[result]}" ,data={'imgPath':path})
        return levelTwoRequest.json()
    else:
        return jsonify(
            status='fail',
            data=None
        )

def initData():
    redirectPorts[0]=5001


if __name__ == '__main__':
    initData()
    app.run(host='0.0.0.0' , port=5000 , debug =True )
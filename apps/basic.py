import os
import uuid
import requests
from flask import Flask, request, json, jsonify
from keras.models import load_model

from method import Model

model = Model(23 , 224 ,0.0001 ,'../Models/basic.h5')

app = Flask(__name__)
UPLOAD_FOLDER = '../imgs'
redirectPorts ={}
redirectPorts = json.load(open('ip.json'))

data = {}
data = json.load((open('../Labels/basic.json')))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['img']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        path = os.path.join(UPLOAD_FOLDER, f_name)
        file.save(path)
        resultFromModel = model.simulation(path)

        basicDeasese = []
        secondDeasese = []
        print(resultFromModel)

        for i in range(len(resultFromModel)):
            basicDeasese.append(int(resultFromModel[i]))

        resultDict = {}
        for result in basicDeasese:
            resultDict[data[str(result)]] = []
            try:
                port = result + 5001
                levelTwoRequest = requests.post(f'http://{redirectPorts[str(result)]}:{port}', data={'imgPath': path})
                resultDict[data[str(result)]] = levelTwoRequest.json()['data']
            except:
                pass

        return jsonify({'status': 'success', 'Data': resultDict})
    else:
        return jsonify(status='fail', data=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5000 , debug =True )
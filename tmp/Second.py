import os
import uuid

from flask import Flask, request, json, jsonify
from keras.models import load_model

from method import Model
app = Flask(__name__)
UPLOAD_FOLDER = './imgs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = Model({{shape}} ,  224 ,0.0001 , "../Models/{{fileName}}.h5")
data={}
data = json.load(open('../Labels/{{fileName}}.json'))
@app.route('/', methods=['GET', 'POST'])

def upload():
    if request.method == 'POST':

        path = request.form.get('imgPath')
        result =model.simulation(path)
        resultList =[]
        for i in range(len(result)):
            resultList.append(data[str(result[i][0])])
        return jsonify(data= resultList)
    else:
        return jsonify(data=None)



if __name__ == '__main__':
    app.run(host='{{ip}}' , port={{port}} , debug =True )

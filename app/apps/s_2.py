import os
import uuid

from flask import Flask, request, json, jsonify
from keras.models import load_model

from method import Model
app = Flask(__name__)
UPLOAD_FOLDER = './imgs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = Model(8 ,  224 ,0.0001 , "../Models/s_2.h5")
data={}
data = json.load(open('../Labels/s_2.json'))
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        path = request.form.get('imgPath')
        result =int(model.simulation(path)[0])
        os.remove(path)
        return jsonify(
            status='success',
            data= data[str(result)]
        )
    else:
        return jsonify(
            status='fail',
            data=None
        )



if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5003 , debug =True )
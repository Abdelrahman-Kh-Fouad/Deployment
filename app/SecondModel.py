
import os
import uuid

from flask import Flask, request, json, jsonify
from keras.models import load_model

from method import Model
app = Flask(__name__)
UPLOAD_FOLDER = './imgs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = Model(8 ,  224 ,0.0001 , "Layer2-0skindiseases.h5")
data={}

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        path = request.form.get('imgPath')
        result =int(model.simulation(path)[0])
        os.remove(path)
        return jsonify(
            status='success',
            data= data[result]
        )
    else:
        return jsonify(
            status='fail',
            data=None
        )

def initData():
    list = ['Acne' , ' Hidradenitis suppurativa' , 'Infantile acne' , ' Milia images' , '  Perioral dermatitis' , '   Rhinophyma' , 'Rosacea' , 'Steroid acne']
    for i in range (8):
        data[i] = list[i]

if __name__ == '__main__':
    initData()
    app.run(host='localhost' , port=5001 , debug =True )

import os
import uuid

from flask import Flask, request, json, jsonify
from keras.models import load_model

from method import Model
app = Flask(__name__)

model = Model( 7 ,  224 ,0.0001 , "../Models/s_2.h5")
labelDict = {}
labelDict = json.load(open('../Labels/s_2.json'))

@app.route('/', methods=['GET', 'POST'])
def upload():
    data  = []
    if request.method == 'POST':
        try :
            path = request.form.get('imgPath')
            resultFromModel = model.simulation(path)
            resultList = []
            for result in resultFromModel:
                resultList.append({'disease': data[str(result.index)], 'probability': result.prop})
            os.remove(path)
            data = resultList
        except:
            data = []

    return jsonify(data= data)

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5003 , debug =True )
import os
import uuid
import requests
from docutils.nodes import status
from flask import Flask, request, json, jsonify
from keras.models import load_model
from method import Model

model = Model( {{shape}} , 224 ,0.0001 ,'../Models/{{ fileName }}.h5')

app = Flask(__name__)
UPLOAD_FOLDER = '../imgs'
redirectIP ={}
redirectIP = json.load(open('ip.json'))

labelDict = {}
labelDict = json.load((open('../Labels/{{ fileName }}.json')))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    note =""
    data = []
    status = request.method == 'POST'
    if status:
        ip_address = request.remote_addr
        try :
            file = request.files['img']
            extension = os.path.splitext(file.filename)[1]
            f_name = str(uuid.uuid4()) + extension
            path = os.path.join(UPLOAD_FOLDER, f_name)
            file.save(path)
        except:
            status = False
            note ="request body isn't in the valid format"

        if status :
            resultFromModel = model.simulation(path)
            print(resultFromModel)
            resultDict = []
            for result in resultFromModel:
                secondResult =[]
                try:
                    port = result.index + 5001
                    levelTwoRequest = requests.post(f'http://{redirectIP[str(result.index)]}:{port}', data={'imgPath': path})
                    secondResult =  levelTwoRequest.json()['data']
                except:
                    note = "some models doesn't exist"
                resultDict.append({'category':labelDict[str(result.index)] , 'propability' : result.prop , 'predection' : secondResult})

            os.remove(path)
            data = resultDict
    else :
        note = 'wrong request'
    status = 'success' if status else 'faild'
    return jsonify({
        'status': status,
        'data': data ,
        'note':note
    })



# def SendIP():
#     r = requests.request(url = 'http://checkip.amazonaws.com' , method='GET')
#     ip = r.text
#     r = requests.request(url= 'http://dls-grad.spider-te8.com/api/v1/storeNewIPAddress' , method='POST' , )

if __name__ == '__main__':
    app.run(host='{{ip}}' , port= {{port}} , debug =True )

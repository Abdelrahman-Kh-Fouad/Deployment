import copy
import os
import uuid
import requests
from flask import Flask, request, json, jsonify
from method import Model

model = Model( 4 , 224 ,0.0001 ,'../Models/basic.h5')

app = Flask(__name__)
UPLOAD_FOLDER = '../Imgs'
redirectIP ={}
redirectIP = json.load(open('ip.json'))



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    note =""
    data = []
    status = request.method == 'POST'
    if status:
        labelDict = {}
        labelDict = json.load((open('../Labels/basic.json')))
        ip_address = request.remote_addr
        try :
            imgFile = request.files['img']
            imgFileBytes = imgFile.read()
            imgExt = os.path.splitext(imgFile.filename)[1]
        except:
            status = False
            note ="request body isn't in the valid format"

        if status :
            resultFromModel = model.simulation(imgFileBytes)
            print(resultFromModel)
            resultDict = []
            for result in resultFromModel:
                secondResult =[]
                try:
                    port = result.index + 5001
                    levelTwoRequest = requests.post(
                        f'http://{redirectIP[str(result.index)]}:{port}',
                        files={'img': imgFileBytes}
                    )
                    secondResult =  levelTwoRequest.json()['data']
                except:
                    note = "some models doesn't exist"
                resultDict.append({
                    'category':labelDict[str(result.index)] ,
                    'propability' : result.prop ,
                    'predection' : secondResult
                })

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
    app.run(host='0.0.0.0' , port= 5030 , debug =False )

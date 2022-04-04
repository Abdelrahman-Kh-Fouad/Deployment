import copy
import os
import uuid
import requests
from flask import Flask, request, json, jsonify
from method import Model

model = Model( 4 , 224 ,0.0001 ,'../Models/basic.h5')
m= [None for i in range(23)]
m[0] = Model(9 ,224 , 0.0001 , '../Models/s_0.h5')
m[1] = Model(18 , 244 , 0.0001 , '../Models/s_1.h5')
m[2] = Model(4 , 244 , 0.0001 , '../Models/s_2.h5')
m[3] = Model(4 , 244 , 0.0001 , '../Models/s_3.h5')
app = Flask(__name__)
UPLOAD_FOLDER = '../Imgs'
redirectIP ={}
redirectIP = json.load(open('ip.json'))



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    for i in m :
        print(i)
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
            img = imgFileBytes 
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
                print(result)
                try:
                    ind =result.index
                    secondResult.append( m[ind].simulation(img))
                    print(secondResult)
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
    app.run(host='0.0.0.0' , port= 5000 , debug =True )

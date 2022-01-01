import os
import subprocess

import toml
import json
import jinja2
class app :
    def __init__(self , name ,  modelUrl , labelName ,shape  ):
        self.name = name
        self.modelUrl = modelUrl
        self.labelName = labelName
        if self.name == 'basic':
            self.fileName = 'basic'
        else:
            self.fileName = f's_{name}'
        self.shape =shape

    def DownloadModel(self):
        if not (f'{self.fileName}.h5' in modelsAlready):
            print(f'Downloading {self.fileName}.h5')
            subprocess.run(f'./Scripts/down.sh {self.modelUrl} ./Models/{self.fileName}.h5' , shell=True )

    def MakeJson(self):
        labelDict = {}
        labelTxt = open(f'./Labels/{self.labelName}')
        lines = labelTxt.readlines()
        for i in range(0 , len(lines) ,2 ):
            labelDict[int(lines[i+1].strip())] = lines[i].strip()
        with open(f'./Labels/{self.fileName}.json' , 'w+') as fp:
            json.dump(labelDict , fp)

    def MakeCode(self):
        jinjaEnv = jinja2.Environment(loader=jinja2.FileSystemLoader('tmp'))
        templeteName = None
        if self.name == 'basic':
            templeteName = 'Basic.py'
        else :
            templeteName = "Second.py"
        templete = jinjaEnv.get_template(templeteName)
        port = 5000

        if self.name !='basic':
            port+=int(self.name )+1

        file = templete.render({ 'ip': '0.0.0.0' , 'port': port , 'fileName':self.fileName , 'shape':self.shape})
        f = open(f"./apps/{self.fileName}.py", "w+")
        f.write(file)
        f.close()

    def Create(self):
        self.DownloadModel()
        self.MakeJson()
        self.MakeCode()



def MakeDirs():
    dirs = ['Models' , 'imgs']
    for dir in dirs :
        subprocess.run(f'mkdir {dir}' ,shell=True)

if __name__ == '__main__':
    MakeDirs()
    file = toml.load('configuration.toml')
    ip ={}
    apps = []
    for tag in file :
        if tag == 'Basic':
            apps.append(app('basic' ,file[tag]['model'] , file[tag]['label'] , file[tag]['shape']))
            ip[-1] = file[tag]['ip']

        if tag =='Second':
            for levelTwo in file[tag]:
                apps.append(app( levelTwo , file[tag][levelTwo]['model'] , file[tag][levelTwo]['label'], file[tag][levelTwo]['shape']))
                ip[int(levelTwo)] = file[tag][levelTwo]['ip']

    global modelsAlready
    modelsAlready = set()
    for file in os.listdir('./Models'):
        modelsAlready.add(file)

    with open(f'./apps/ip.json', 'w+') as fp:
        json.dump(ip, fp)
    for i in apps:
        i.Create()

    print('Done')
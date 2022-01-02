import os
import subprocess
import toml
import json
import jinja2

class app :
    def __init__(self , name ,  modelUrl , labelName , shape , redownload:bool ):
        self.name = name
        self.modelUrl = modelUrl
        self.redownload = bool(redownload)
        self.labelName = labelName
        if self.name == 'basic':
            self.fileName = 'basic'
        else:
            self.fileName = f's_{name}'
        self.shape =shape

    def DownloadModel(self):
        modelsAlready =set(file for file in os.listdir('./Models'))
        if not (f'{self.fileName}.h5' in modelsAlready) or self.redownload:
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
    tomFile = toml.load('configuration.toml')
    ip ={}
    apps = []
    for tag in tomFile :
        if tag == 'Basic':
            apps.append(
                app(
                    'basic',
                    tomFile[tag]['model'] ,
                    tomFile[tag]['label'] ,
                    tomFile[tag]['shape'] ,
                    int(tomFile[tag]['redownload'])
                ))
            ip[-1] = tomFile[tag]['ip']

        if tag =='Second':
            for levelTwo in tomFile[tag]:
                apps.append(
                    app(
                        levelTwo ,
                        tomFile[tag][levelTwo]['model'] ,
                        tomFile[tag][levelTwo]['label'] ,
                        tomFile[tag][levelTwo]['shape'] ,
                        int(tomFile[tag][levelTwo]['redownload'])
                    ))
                ip[int(levelTwo)] = tomFile[tag][levelTwo]['ip']

    with open(f'./apps/ip.json', 'w+') as fp:
        json.dump(ip, fp)

    for i in apps:
        i.Create()

    print('Done')
import subprocess
import toml
import json
from AppInstance import App

def MakeDirs():
    dirs = ['Models' , 'Imgs' , 'Imports' , 'Models']
    for dir in dirs :
        subprocess.run(f'mkdir {dir}' ,shell=True)

if __name__ == '__main__':

    MakeDirs()
    tomFile = toml.load('configuration.toml')
    apps = []
    serversIps = {}
    for tag in tomFile :
        if tag == 'Basic':
            apps.append(
                App(
                    'basic',
                    tomFile[tag]['model'] ,
                    serversIps[tomFile[tag]['parent']]
                ))
        if tag =='Second':
            for levelTwo in tomFile[tag]:
                apps.append(
                    App(
                        levelTwo ,
                        tomFile[tag][levelTwo]['model'] ,
                        serversIps[tomFile[tag][levelTwo]['parent']]
                    ))


        if tag == 'Servers':
            serversNum = tomFile[tag]['number']
            for server in tomFile[tag]:
                if server =='number':
                    continue
                serversIps[int(server)] = tomFile[tag][server]['ipv4']

    with open('./Apps/sets.json', 'w+') as fp:
        json.dump(serversIps, fp)
    ips ={}
    basicIn:bool = False
    for app in apps:
        if app.name=='basic' and app.isSameIp :
            basicIn =True
        if app.name != 'basic':
            if app.isSameIp:
                ips[app.name] = '0.0.0.0'
            else :
                ips[app.name] = app.toBuildIp
        app.Create()
    if basicIn :
        with open('./Apps/ip.json' ,'w+') as fp :
            json.dump(ips , fp)


    print('Done')

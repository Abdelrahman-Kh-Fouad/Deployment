import os
import subprocess
import toml
import json
import jinja2
from AppInstance import App

def MakeDirs():
    dirs = ['Models' , 'Imgs']
    for dir in dirs :
        subprocess.run(f'mkdir {dir}' ,shell=True)

if __name__ == '__main__':

    MakeDirs()
    tomFile = toml.load('configuration.toml')
    ip ={}
    apps = []
    serversIps = {}
    for tag in tomFile :
        if tag == 'Basic':
            apps.append(
                App(
                    'basic',
                    tomFile[tag]['model'] ,
                    tomFile[tag]['label'] ,
                    tomFile[tag]['shape'] ,
                    int(tomFile[tag]['redownload']),
                    serversIps[tomFile[tag]['parent']]
                ))
            ip[-1] = tomFile[tag]['ip']

        if tag =='Second':
            for levelTwo in tomFile[tag]:
                apps.append(
                    App(
                        levelTwo ,
                        tomFile[tag][levelTwo]['model'] ,
                        tomFile[tag][levelTwo]['label'] ,
                        tomFile[tag][levelTwo]['shape'] ,
                        int(tomFile[tag][levelTwo]['redownload']),
                        serversIps[tomFile[tag][levelTwo]['parent']]
                    ))
                ip[int(levelTwo)] = tomFile[tag][levelTwo]['ip']

        if tag == 'Servers':
            serversNum = tomFile[tag]['number']
            for server in tomFile[tag]:
                if server =='number':
                    continue
                serversIps[int(server)] = tomFile[tag][server]['ipv4']

    with open(f'./Apps/ip.json', 'w+') as fp:
        json.dump(ip, fp)

    for i in apps:
        i.Create()

    print('Done')
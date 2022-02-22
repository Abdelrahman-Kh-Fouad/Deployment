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

    with open(f'./Apps/ip.json', 'w+') as fp:
        json.dump(ip, fp)

    for i in apps:
        i.Create()

    print('Done')
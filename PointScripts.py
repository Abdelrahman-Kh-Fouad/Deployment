import sys
import os
import subprocess

def RunBash(scriptFilebath:str)->None:
    subprocess.run(f'chmod +x {scriptFilebath}',shell=True)
    subprocess.call(f'{scriptFilebath}' ,shell=True)

if __name__ == '__main__':
    currentPath = sys.path[0]
    for scriptFileName in os.listdir(currentPath+'/PointScripts'):
        RunBash(currentPath+'/'+'PointScripts' + '/' +scriptFileName)
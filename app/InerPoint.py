import re
import subprocess
import sys
import os
if __name__ == '__main__':

    url = "https://drive.google.com/file/d/1Me7qeEZ5K2ECMPTiqICDQurx_wHARXgm/view"
    modeName = 'mymodel.h5'
    currentPath = sys.path[0]
    print(os.listdir(currentPath))
    if not (modeName in os.listdir(currentPath)):
        fileName = re.findall( r'https://drive.google.com/file/d/(.*)/view' ,url)[0]
        download = subprocess.run(f'{sys.path[0]}/InerPointScripts/wget_gdrive.sh {fileName}  {modeName}',shell=True)
        # while download.stdout :
        #     print(download.stdout)
    subprocess.run('gunicorn -b 0.0.0.0:8000 app:app',shell=True)
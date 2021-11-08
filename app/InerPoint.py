import re
import subprocess
import sys
import os 
url = "https://drive.google.com/file/d/1Me7qeEZ5K2ECMPTiqICDQurx_wHARXgm/view"

fileName = re.findall( r'https://drive.google.com/file/d/(.*)/view' ,url)[0]    
download = subprocess.run(f'{sys.path[0]}/InerPointScripts/wget_gdrive.sh {fileName} mymodel.h5' ,shell=True)
# while download.stdout : 
#     print(download.stdout)

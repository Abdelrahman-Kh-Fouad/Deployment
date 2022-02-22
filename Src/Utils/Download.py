import subprocess
import os
def DownloadFromDrive(id:str , pathAndFileName:str):
    subprocess.run(f'./Src/Utils/down.sh {id} {pathAndFileName} > logs.out' , shell=True)
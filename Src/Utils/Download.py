import subprocess
def DownloadFromDrive(id:str , pathAndFileName:str):
    subprocess.run(f'./down.sh {id} {pathAndFileName} > logs.out' , shell=True)
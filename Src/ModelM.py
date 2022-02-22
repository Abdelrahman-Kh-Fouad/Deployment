import json

from Utils import RAR
from Utils import Download
from rarfile import RarFile
from Utils import Json
import os

class ModelMan :
    def __init__(self ,googleDriveId:str , name:str , fileName:str):
        self.name = name
        self.fileName = fileName
        self.googleDriveId = googleDriveId

    def DownloadRAR(self):
        flag:bool = True
        try :
            flag:bool = not RAR.Check(f'Imports/{self.name}.rar')
        except:
            pass
        while flag:
            print(f'Download Model for {self.name}')
            Download.DownloadFromDrive(self.googleDriveId , f'Imports/{self.fileName}.rar')
            flag = flag and not RAR.Check(f'Imports/{self.fileName}.rar')

    def Extract(self):
        rarF = RarFile(f'Imports/{self.name}.rar')
        if len(rarF.namelist()) !=2 :
            warn = f'Error in rar file of model {self.name}'
            raise ValueError(warn)
        else :
            cnt =0
            for inner in rarF.namelist():
                ext = os.path.splitext(inner)[1]

                if ext.lower() == '.json' :
                    cnt +=1
                    fileInBytes = rarF.read(inner)
                    dic = Json.ConvertFromBinToJson(fileInBytes , True)
                    self.shape = len(dic)
                    with open(f"./Labels/{self.fileName}.json", "w") as f:
                        json.dump(dic , f)

                elif ext.lower() == '.h5' :
                    cnt+=1
                    fileInBytes = rarF.read(inner)
                    with open(f'./Models/{self.fileName}.h5' ,"ab") as f :
                        f.write(fileInBytes)

            if cnt !=2 :
                warn = f'Error in rar file (there are files not in same extension) on model {self.name}'
                raise  ValueError(warn)

    def CreateRar(self):
        self.DownloadRAR()
        self.Extract()
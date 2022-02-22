from Utils import RAR
from Utils import Download
from rarfile import RarFile
from Utils import Json
import os
class ModelMan :
    def __init__(self ,googleDriveId:str , name:str):
        self.name = name
        self.googleDriveId = googleDriveId

    def DownloadRAR(self):
        flag:bool = True
        while flag:
            print(f'Download Model for {self.name}')
            Download.DownloadFromDrive(self.googleDriveId , f'Imports/{self.name}.rar')
            flag = flag and not RAR.Check(f'Imports/{self.name}.rar')

    def Extract(self):
        rarF = RarFile(f'Imports/{self.name}.rar')
        if len(rarF.namelist()) !=2 :
            raise ValueError(f'Error in rar file of model {self.name}')
        else :
            cnt =0
            for inner in rarF.namelist():
                ext = os.path.splitext(inner)[1]

                if ext.lower() == '.json' :
                    cnt +=1
                    fileInBytes = rarF.read(inner)
                    dic = Json.ConvertFromBinToJson(fileInBytes , True)
                    self.shape = len(dic)
                    with open(f"./Labels/{self.name}.json", "ab") as f:
                        f.write(dic)

                elif ext.lower() == '.h5' :
                    cnt+=1
                    fileInBytes = rarF.read(inner)
                    with open(f'./Models/{self.name}.h5' ,"ab") as f :
                        f.write(fileInBytes)

            if cnt !=2 :
                raise  ValueError(f'Error in rar file (there are files not in same extension) on model {self.name}')

    def CreateRar(self):
        self.DownloadRAR()
        self.Extract()
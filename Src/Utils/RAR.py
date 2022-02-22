import patoolib
from rarfile import RarFile

def Unrar(rarFilePath:str , outPath:str):
    patoolib.extract_archive(rarFilePath, outdir=outPath)

def Check(path:str)->bool:
    res =False
    try :
        file = RarFile(path ,'r')
        del file
        res = True
    except :
        pass
    return res


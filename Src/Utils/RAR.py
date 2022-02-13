import patoolib
def Unrar(rarFilePath:str , outPath:str):
    patoolib.extract_archive(rarFilePath, outdir=outPath)


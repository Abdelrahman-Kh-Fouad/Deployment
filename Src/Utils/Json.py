import json
def ConvertFromBinToJson(content:bytes , reverse:bool):
    dic = json.loads(content.decode("utf-8") )
    if reverse:
        new ={}
        for i , j in dic.items():
            new[j] = i ;
        dic = new
    return dic

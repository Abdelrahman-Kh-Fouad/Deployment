import requests

def MyIpv4():
    response = requests.get('https://api.ipify.org').content.decode('utf8')
    return response
#http://dls-grad.spider-te8.com/api/v1/storeNewIPAddress

def SendMyIpToServer(serverUrl:str):
    response = requests.request(url= serverUrl ,
                                method='POST' ,
                                data={'ip_address':MyIpv4()})
    print(response.json()['msg'])

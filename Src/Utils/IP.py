import requests

def MyIpv4():
    response = requests.get('https://api.ipify.org').content.decode('utf8')
    return response
import os
import json
import requests
import sys
import time
import pprint
if __name__ == '__main__':
    url = sys.argv[1]
    print(url)
    currentPath = os.getcwd() +  '/Diseases'
    for generlPath in os.listdir(currentPath):
        for spPath in os.listdir(currentPath+'/'+generlPath):
            img = {'img':open(f'{currentPath}/{generlPath}/{spPath}' , 'rb')}
            #print(img)
            before = time.time()
            request = requests.post(url , files=img)
            after = time.time()
            deff = "{:.2f}".format(after -before)
            print(f'Time -> {deff}s')
            print(f'{generlPath}/{spPath}')
            response = request.json()
            print(request.status_code)
            try:
                print(json.dumps(response,sort_keys=True, indent=4))
                print(60 *'-')
            except:
                pass

    

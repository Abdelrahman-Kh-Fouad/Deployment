import os
import json
import requests
import sys
import time
import pprint
from jinja2 import Template

data = '''
{% for response, path ,time  in my_list %}
<p style ="text-align:center">
<img height = 500 width = 600 src ="{{ path }}">
</p>
<h3 style ="text-align:center "> Response time = {{ time }}s </h3>

```json
{{ response }}
```
------- 
{% endfor %}

'''
tm = Template(data)


def go(path):
    img = {'img':open(path , 'rb')}
    #print(img)
    before = time.time()
    request = requests.post(url , files=img)
    after = time.time()
    deff = "{:.2f}".format(after -before)
    print(f'Time -> {deff}s')
    print(path)
    res =()
    response = request.json()
    print(request.status_code)
    try:
        path = path.strip().replace(' ','\ ')
        print(json.dumps(response,sort_keys=True, indent=4) )
        os.system(f"viu -1 -w 60 -h 30 {path}")
        print(60 *'-')
        res = (json.dumps(response,sort_keys=True, indent=4) , path ,deff )
    except:
        pass
    return  res


if __name__ == '__main__':
    url = sys.argv[1]
    print(url)
    currentPath = './Diseases'
    list = []
    for generlPath in os.listdir(currentPath):
        try :
            for spPath in os.listdir(currentPath+'/'+generlPath):
                list.append(go(f"{currentPath}/{generlPath}/{spPath}"))
                 
        except:
            list.append(go(f"{currentPath}/{generlPath}"))
    res =tm.render(my_list = list )
    f = open("report.md" , 'w+')
    f.write(res)
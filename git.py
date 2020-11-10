import requests
import json

WebPage = 'https://api.github.com'
Person ='SergeySysoev386'

request = requests.get(f'{WebPage}/users/{Person}/repos')

with open('git.json', 'w') as f:
    json.dump(request.json(), f)
    for i in request.json():
        print(i['name'])
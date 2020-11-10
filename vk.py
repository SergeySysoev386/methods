import requests
import json
WebPage = 'https://api.vk.com/method/groups.get?v=5.52&access_token=39a63b3415cf1da39da9236179af5748d7eb543f0229c72283807fa9e32a44477dda688f7d8afed152648'
token = '39a63b3415cf1da39da9236179af5748d7eb543f0229c72283807fa9e32a44477dda688f7d8afed152648'
vk = requests.get(f'{WebPage}')
vk.json()
with open('vk.json', 'w') as f:
    json.dump(vk.json(), f)
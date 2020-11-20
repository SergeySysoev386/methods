from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
main_link = 'https://lenta.ru/'
response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)
lenta = dom.xpath("//time[@class='g-time']/..")

lenta_list = []
for i in lenta:
    lenta_dict = {}
    source = 'lenta.ru'
    title = i.xpath(".//time[@class='g-time']/../text()")
    link = i.xpath(".//time[@class='g-time']/../@href")
    time_stamp = i.xpath(".//time[@class='g-time']/text()")

    lenta_dict['название источника'] = source[0]
    lenta_dict['наименование новости'] = title[0].replace('\xa0', ' ')
    lenta_dict['ссылка на новость'] = link[0]
    lenta_dict['тайм стемп'] = time_stamp[0]

    lenta_list.append(lenta_dict)
pprint(lenta_list)
client = MongoClient('127.0.0.1', 27017)
db = client['Lenta']
lenta_ru = db.lenta_ru
lenta_ru.insert_many(lenta_list)

from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
main_link = 'https://yandex.ru/news/'
response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)
yandex = dom.xpath("//div[@class='news-card__inner'] | //div[@class='mg-grid__col mg-grid__col_xs_4']")
yandex_list = []
for i in yandex[:5]:
    yandex_dict = {}
    source = i.xpath(".//span[@class='mg-card-source__source']/a/text()")
    title = i.xpath(".//h2[@class='news-card__title']/text()")
    link = i.xpath(".//a[@class='news-card__link']/@href")
    time_stamp = i.xpath(".//span[@class='mg-card-source__time']/text()")

    yandex_dict['название источника'] = source[0]
    yandex_dict['наименование новости'] = title[0]
    yandex_dict['ссылка на новость'] = link[0]
    yandex_dict['тайм стемп'] = time_stamp[0]

    yandex_list.append(yandex_dict)
pprint(yandex_list)
client = MongoClient('127.0.0.1', 27017)
db = client['Yandex']
yandex_ru = db.yandex_ru
yandex_ru.insert_many(yandex_list)

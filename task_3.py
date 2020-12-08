import requests
from pprint import pprint
import re
from bs4 import BeautifulSoup as bs
main_link = 'https://hh.ru/search/vacancy'
vacancy_hh = 'Python'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
}


n_page = 0
vacancies = []
while True:

    params = {
        'L_is_autosearch':'false',
        'area': '2',
        'clusters':'true',
        'enable_snippets':'true',
        'text': vacancy_hh,
        'page': n_page

    }
    response = requests.get(main_link, params=params, headers=headers)


    if response.status_code == 200:
        dom = bs(response.text, 'html.parser')


        vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

        for vacancy in vacancy_list:
            vacancy_data = {}
            vacancy_name = vacancy.find('a').text
            vacancy_link = vacancy.find('a')['href']
            vacancy_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            regex_num = re.compile('\d+')
            s = regex_num.search(vacancy_link)
            vacancy_id = vacancy_link[s.start():s.end()]

            if not vacancy_salary:
                salary_min = None
                salary_max = None
                salary_currency = None
            else:
                vacancy_salary = vacancy_salary.getText().replace(u'\xa0', u'')
                vacancy_salary = re.split(r'\s|-', vacancy_salary)
                if vacancy_salary[0] == 'до':
                    salary_min = None
                    salary_max = float(vacancy_salary[1])
                    salary_currency = vacancy_salary[2]
                elif vacancy_salary[0] == 'от':
                    salary_max = None
                    salary_min = float(vacancy_salary[1])
                    salary_currency = vacancy_salary[2]
                else:
                    salary_max = float(vacancy_salary[1])
                    salary_min = float(vacancy_salary[0])
                    salary_currency = vacancy_salary[2]

            vacancy_data['_id'] = int(vacancy_id)
            vacancy_data['name'] = vacancy_name
            vacancy_data['vacancy_link'] = vacancy_link
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['currency'] = salary_currency

            vacancies.append(vacancy_data)


    if dom.find(text='дальше'):
        n_page += 1
    else:
        break

# pprint(vacancies)
import numpy as pd
import pandas as pd
df = pd.DataFrame(vacancies)


from pymongo import MongoClient
client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
vacancies_hh = db.head
list = vacancies


maxsalary = 100000

for vacancy in vacancies_hh.find({'$or': [{'salary_max': {'$gt': maxsalary}}, {'salary_min': {'$gt': maxsalary}}]}):
     pprint(vacancy)



x = 0

for index, row in df.iterrows():
    x = vacancies_hh.find({'_id': row['_id']}).count()
    if x == 0:
        vacancies_hh.insert_one({'_id': row['_id'], 'currency': row['currency'], 'name': row['name'], 'salary_max': row['salary_max'],
        'salary_min': row['salary_min'], 'vacancy_link': row['vacancy_link']})
        print('Вакансия успешно добавлена')
    else:
        print('Вакансия уже существует')
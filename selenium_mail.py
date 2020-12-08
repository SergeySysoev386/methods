from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://mail.ru/')
login_button = driver.find_element_by_id('mailbox:login-input')
login_button.send_keys('study.ai_172')
pass_button = driver.find_element_by_id('mailbox:submit-button')
pass_button.click()
time.sleep(1)
pass_field = driver.find_element_by_id('mailbox:password-input')
pass_field.send_keys('NextPassword172')

enter_button = driver.find_element_by_id('mailbox:submit-button')
enter_button.click()
time.sleep(5)
driver.get('https://e.mail.ru/inbox')
mail_list = set()
while True:
    letters_list = len(mail_list)
    time.sleep(5)
    scroller = ActionChains(driver)
    letters = driver.find_elements_by_class_name('js-letter-list-item')
    for letter in letters:
        mail_list.add(letter.get_attribute('href'))
    letters_listnew = len(mail_list)
    if letters_list == letters_listnew:
        break
    scroller.move_to_element(letters[-1])
    scroller.perform()
data = []

for elem in mail_list:
    mails = {}
    time.sleep(3)
    driver.get(elem)
    time.sleep(5)
    from_who = driver.find_element_by_class_name('letter-contact').text
    letter_date = driver.find_element_by_class_name('letter__date').text
    header = driver.find_element_by_tag_name('h2').text
    content = driver.find_element_by_class_name('js-helper').text

    mails['Заголовок'] = header
    mails['Содержимое письма'] = content
    mails['Дата получения'] = letter_date
    mails['Отправитель'] = from_who

    data.append(mails)
pprint(data)
driver.quit()
client = MongoClient('127.0.0.1', 27017)
db = client['letters_list']
letters_collection = db.letters_collection
letters_collection.insert_many(data)

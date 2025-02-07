#Парсер для aliexpress секунд 13.
import json
import time
import random
import threading
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from AlgoritmAli import sorting_products


file_lock = threading.Lock()

def sort(products):
    # with open('Products_ozon.json','r',encoding='UTF-8') as file:
    #     products = json.load(file)
    weights = sorting_products(products)
    onion = list(zip(weights, products))
    onion.sort(key=lambda x: (x[0], int(x[1]['Цена'].replace('₽','').replace('\xa0',''))), reverse=True)
    s = []
    for i in range(4):
        s.append(onion[i][1])
    with open("BeautifulAliexpressProducts.json", 'w', encoding="UTF-8") as file:
        json.dump(s,file,indent=4,ensure_ascii=False)


def parser(html:str ='') -> dict:
    '''Функция которая ищет всю информацию про товары(кроме ссылки на товар)'''
    
    soup = BeautifulSoup(html, 'html.parser')
    all = soup.find_all('div', class_="red-snippet_RedSnippet__container__hyohn9")

    s = []

    for link in all:
        product_info = {}
        try:
            product_info['Название'] = product_info.setdefault('Название', link.find('div', class_='red-snippet_RedSnippet__contentWithAside__hyohn9').find('div', 
            class_='red-snippet_RedSnippet__trustAndTitle__hyohn9').find('div',class_='red-snippet_RedSnippet__title__hyohn9').text)
            product_info['Цена'] = product_info.setdefault('Цена', link.find('div', class_='red-snippet_RedSnippet__price__hyohn9').find('div', 
            class_='red-snippet_RedSnippet__priceNew__hyohn9').find('span').text)
            product_info['Ссылка'] = product_info.setdefault('Ссылка','https:' +  link.find('div').find('a')['href'])
            product_info['Фото'] = product_info.setdefault('Фото', link.find('div', class_='gallery_Gallery__gallery__15bdcj').find('div', class_='gallery_Gallery__picList__15bdcj'
            ).find('div').find('img')['src'])
            product_info['Звёзды'] = product_info.setdefault('Звёзды', link.find('div', class_='red-snippet_RedSnippet__trust__hyohn9').find('div').find('span').text)
            product_info['Оценки'] = product_info.setdefault('Оценки',  None) #Не даёт
            product_info['Время'] = product_info.setdefault('Время', None) # А этого нету
            s.append(product_info)
        except:
            continue
    
    # with open('Ali.json', 'w', encoding="UTF-8") as file:
    #     json.dump(s,file,indent=4,ensure_ascii=False)
    sort(s)

def get_products_links(item_name:str = 'Айфон 15') -> None:
    '''функция принимает запрос от пользователя и начинает суету'''
    t = random.uniform(2, 5)
    options = uc.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    
    options.add_argument('--headless')  # Включаем headless-режим
    options.add_argument('--no-sandbox')  # Отключаем sandbox для повышения стабильности
    options.add_argument('--disable-dev-shm-usage')  # Решает проблемы с памятью в headless-режиме

    user_agent = [
        "Mozilla/5.0 (Linux; Android 7.0; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4143.7 Mobile Safari/537.36 Chrome-Lighthouse",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 9; Redmi Note 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.111 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 9.0; Pixel 2 XL Build/PPP4.180612.004; Windows 10 Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3552.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 9; FLA-LX1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; Redmi Note 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36",
        ]
    options.add_argument(f'--user-agent={user_agent[random.randint(0,6)]}')
    with file_lock:
        driver = uc.Chrome(use_subprocess=False,options=options, version_main=132)
        driver.implicitly_wait(t)

        driver.get(url='https://aliexpress.ru')
        time.sleep(t)

    find_input = driver.find_element(By.NAME, 'SearchText')
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(t)

    find_input.send_keys(Keys.ENTER)
    time.sleep(t)

    html = str(driver.page_source)
    parser(html)


def mainAli(item_name='Телефон'):
    get_products_links(item_name)


if __name__=='__main__':
    main()
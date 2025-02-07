#Парсер для озона который сохраняет всю информацию о первых 12+- выпавших продуктов в json файл
#Он не запуститься если у вас не установлен драйвер на хром
import json
import time
import threading
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Algoritm import sorting_products

file_lock = threading.Lock()

def sort(products):
    # with open('Products_ozon.json','r',encoding='UTF-8') as file:
    #     products = json.load(file)
    weights = sorting_products(products)
    onion = list(zip(weights, products))
    onion.sort(key=lambda x: (x[0], int(x[1]['Цена'].replace('₽','').replace('\u2009',''))), reverse=True)
    s = []
    for i in range(4):
        s.append(onion[i][1])
    with open("BeautifulOzonProducts.json", 'w', encoding="UTF-8") as file:
        json.dump(s,file,indent=4,ensure_ascii=False)
        

def colleсt_product_info(html:str ='') -> dict:
    '''Функция которая ищет всю информацию про товары(кроме ссылки на товар)'''
    
    soup = BeautifulSoup(html, 'html.parser')
    all = soup.find_all('div', class_="xi6_23")
    s = []

    for link in all:
        product_info = {}

        product_info['Название'] = product_info.setdefault('Название', link.find('div', class_='xi7_23').find('span', class_="tsBody500Medium").text)
        product_info['Цена'] = product_info.setdefault('Цена', link.find('div',class_='c3024-a0').find_all('span')[1].text)
        product_info['Ссылка'] = product_info.setdefault('Ссылка', 'https://ozon.ru' + link.find('div', class_='xi7_23').find('a', class_="tile-clickable-element")['href'])
        product_info['Фото'] = product_info.setdefault('Фото', link.find('div', class_='i9y_23').find('img')['src'])
        product_info['Звёзды'] = product_info.setdefault('Звёзды', link.find_all('div', class_='yi0_23')[-1].find('span', class_='p6b13-a4').find('span').text)
        product_info['Оценки'] = product_info.setdefault('Оценки', link.find_all('div', class_='yi0_23')[-1].find_all('span', class_='p6b13-a4')[-1].find('span').text)
        product_info['Время'] = product_info.setdefault('Время', link.find('div', class_='b2121-a1').find('div').text)
        s.append(product_info)

    # with open('Products_ozon.json','w', encoding='UTF-8') as file:
    #     json.dump(s, file, indent=4, ensure_ascii=False)
    sort(s)

def get_products_links(item_name:str = 'Айфон 15') -> None:
    '''функция принимает запрос от пользователя и начинает суету'''

    options = uc.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    
    options.add_argument('--headless')  # Включаем headless-режим
    options.add_argument('--no-sandbox')  # Отключаем sandbox для повышения стабильности
    options.add_argument('--disable-dev-shm-usage')  # Решает проблемы с памятью в headless-режиме

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    options.add_argument(f'--user-agent={user_agent}')
    with file_lock:
        driver = uc.Chrome(use_subprocess=False,options=options, version_main=132)
        driver.implicitly_wait(1)

        driver.get(url='https://ozon.ru')
        time.sleep(0.05)

    find_input = driver.find_element(By.NAME, 'text')
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(0.05)

    find_input.send_keys(Keys.ENTER)
    time.sleep(0.05)

    with file_lock:
        current_url = f'{driver.current_url}&sorting=rating'
        driver.get(url=current_url)
        time.sleep(0.05)

    page_sourse = str(driver.page_source)
    colleсt_product_info(page_sourse)

    driver.quit()

def mainOZON(item_name: str):
    get_products_links(item_name)

if __name__=='__main__':
    main()
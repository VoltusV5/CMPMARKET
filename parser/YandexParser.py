#Парсит 16 товаров +-. Скорость примерно 11 сек
import json
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from AlgoritmYA import sorting_products

def sort(products):
    # with open('Products_ozon.json','r',encoding='UTF-8') as file:
    #     products = json.load(file)
    weights = sorting_products(products)
    onion = list(zip(weights, products))
    onion.sort(key=lambda x: (x[0], int(x[1]['Цена'].replace('₽','').replace('\u2009',''))), reverse=True)
    s = []
    for i in range(4):
        s.append(onion[i][1])
    with open("BeautifulYandexProducts.json", 'w', encoding="UTF-8") as file:
        json.dump(s,file,indent=4,ensure_ascii=False)


def parser(html:str):
    soup = BeautifulSoup(html, 'html.parser')
    products_html_div_all = soup.find_all('div',{'data-apiary-widget-name':'@marketfront/SerpEntity'})[1:]
    
    s = []

    for link in products_html_div_all:
        products_info = {
            "Название": None,
            "Ссылка": None,
            "Цена":None,
            "Цена без карты":None,
            "Фото":None,
            'Время': None,
            'Оценки':None,
            'Звёзды':None,
        }
        try:
            products_info['Название'] = link.find('div', {'data-baobab-name':'title'}).text
        except:
            products_info['Название'] = None
        try:
            products_info['Ссылка'] = 'https://market.yandex.ru'+link.find('div', {'data-baobab-name':'title'}).find('a')['href']
        except:
            products_info['Ссылка'] = None
        try:        
            products_info['Цена'] = link.find('div', class_="_3iCDs").find('span', class_='ds-text').text
        except:
            products_info['Цена'] = None
        try:
            products_info["Цена без карты"] = link.find('div', class_="_3BUO3").text
        except:
            products_info['Цена без карты'] = None
        try:
            products_info['Фото'] = link.find('div', {'data-baobab-name':'pictureGallery'}).find('img')['src']
        except:
            products_info['Фото'] = None
        try:
            products_info['Время'] = link.find('div', class_='_3-1X9').find('span', class_='_1yLiV').text
        except:
            products_info['Время'] = None
        try:
            products_info['Оценки'] = link.find('div',class_='_1ENFO').find('div',{'data-baobab-name':'rating'}).find_all('span', class_='ds-text')[-1].text
        except:
            products_info['Оценки'] = None
        try:
            products_info['Звёзды'] = link.find('div',class_='_1ENFO').find('div',{'data-baobab-name':'rating'}).find_all('span', class_='ds-text')[0].text
        except:
            products_info['Звёзды'] = None

        s.append(products_info)
    

    help = []
    for i in range(len(s)):
        if s[i]['Название'] == None:
            help.append(i)

    for i in help:
        del s[i]


    # with open('YandexProducts.json','w', encoding='UTF-8') as file:
    #     json.dump(s,file,indent=4,ensure_ascii=False)
    sort(s)    


def driver(item_name:str = 'Телефон'):
    options = uc.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    
    options.add_argument('--headless')  # Включаем headless-режим
    options.add_argument('--no-sandbox')  # Отключаем sandbox для повышения стабильности
    options.add_argument('--disable-dev-shm-usage')  # Решает проблемы с памятью в headless-режиме

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    options.add_argument(f'--user-agent={user_agent}')

    driver = uc.Chrome(use_subprocess=False,options=options,version_main=132)
    driver.implicitly_wait(0.5)

    url = 'https://market.yandex.ru'
    driver.get(url=url)
    time.sleep(1)

    find_input = driver.find_element(By.NAME, 'text')
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(0.5)

    find_input.send_keys(Keys.ENTER)
    time.sleep(0.5)

    current_url = f'{driver.current_url}&how=rating'
    driver.get(url=current_url)
    time.sleep(1)
    
    html_text = str(driver.page_source)
    driver.quit()
    parser(html_text)

def main():
    driver()


if __name__=='__main__':
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(t2-t1)
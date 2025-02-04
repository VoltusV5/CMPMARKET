#Парсит 16 товаров +-. Скорость примерно 11 сек
import json
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



def parser(html:str):
    soup = BeautifulSoup(html, 'html.parser')
    products_html_div_all = soup.find_all('div',{'data-apiary-widget-name':'@marketfront/SerpEntity'})[1:]
    
    s = []

    for link in products_html_div_all:
        k = link
        products_info = {
            "Название": None,
            "Ссылка": None,
            "Цена с картой яндекс":None,
            "Цена без карты яндекс":None,
            "Фото":None,
        }
        try:
            products_info['Название'] = link.find('div', {'data-baobab-name':'title'}).text
        except:
            products_info['Название'] = None
        link = k
        try:
            products_info['Ссылка'] = 'https://market.yandex.ru'+link.find('div', {'data-baobab-name':'title'}).find('a')['href']
        except:
            products_info['Ссылка'] = None
        link = k
        try:        
            products_info['Цена с картой яндекс'] = link.find('div', class_="_3iCDs").text
        except:
            products_info['Цена с картой яндекс'] = None
        link = k
        try:
            products_info["Цена без карты яндекс"] = link.find('div', class_="_3BUO3").text
        except:
            products_info['Цена без карты яндекс'] = None
        link = k
        try:
            products_info['Фото'] = link.find('div', {'data-baobab-name':'pictureGallery'}).find('img')['src']
        except:
            products_info['Фото'] = None
        s.append(products_info)
    
    with open('YandexProducts.json','w', encoding='UTF-8') as file:
        json.dump(s,file,indent=4,ensure_ascii=False)
        


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
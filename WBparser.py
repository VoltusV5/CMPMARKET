#Парсит 30 карточек вб, за 6-8 секунд. Если какое то значение в словаре не будет найдено то в json файле будет 0!
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
    find_card = soup.find_all('article', class_='product-card')
    s = []

    for link in find_card:
        product_info = {}

        product_info['Название'] = product_info.setdefault('Название', link.find('span', class_='product-card__name').text.strip().replace('/',''))
        product_info['Цена с вб'] = product_info.setdefault('Цена с вб', link.find('ins',class_='price__lower-price').text)
        product_info['Цена без вб'] = product_info.setdefault('Цена без вб', link.find('span',class_='price__wrap').find('del').text)
        product_info['Ссылка'] = product_info.setdefault('Ссылка', link.find('div', class_='product-card__wrapper').find('a')['href'])
        product_info['Фото'] = product_info.setdefault('Фото', link.find('div',class_='product-card__img-wrap').find('img')['src'])
        product_info['Звёзды'] = product_info.setdefault('Звёзды', link.find('p',class_='product-card__rating-wrap').find('span').text)
        product_info['Оценки'] = product_info.setdefault('Оценки', link.find('p',class_='product-card__rating-wrap').find('span', class_='product-card__count').text)
        s.append(product_info)
    
    with open('WBproducts.json', 'w', encoding='UTF-8') as file:
        json.dump(s, file, indent=4, ensure_ascii=False)
        

def driver(item_name:str = 'макасины'):
    options = uc.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    
    options.add_argument('--headless')  # Включаем headless-режим
    options.add_argument('--no-sandbox')  # Отключаем sandbox для повышения стабильности
    options.add_argument('--disable-dev-shm-usage')  # Решает проблемы с памятью в headless-режиме

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    options.add_argument(f'--user-agent={user_agent}')

    driver = uc.Chrome(use_subprocess=False,options=options)
    driver.implicitly_wait(1)

    url = 'https://www.wildberries.ru/'
    driver.get(url=url)
    time.sleep(0.05)

    find_input = driver.find_element(By.ID, 'searchInput')
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(0.05)

    find_input.send_keys(Keys.ENTER)
    time.sleep(2.5)

    html_code = str(driver.page_source)

    parser(html_code)

    driver.quit()

def main():
    driver()


if __name__=='__main__':
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(t2-t1)
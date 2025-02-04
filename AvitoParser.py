import json
import random
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def parser(text:str):
    soup = BeautifulSoup(text, 'html.parser')
    products = soup.find_all('div', {'data-marker':'item'})
    s = []
    
    for link in products:
        info_products = {
        "Цена":None,
        "Название":None,
        "Фото":None,
        "Ссылка":None,
    }
        info_products['Название'] = link.find('h3').text
        info_products['Ссылка'] = 'https://avito.ru' + str(link.find('a', {"data-marker":"item-title"})['href'])
        try:
            info_products['Фото'] = link.find('img', class_='photo-slider-image-xjG6U')['src']
        except:
            try:
                info_products['Фото'] = link.find('div', class_='image-frame-wrapper-_NvbY')['src']
            except:
                info_products['Фото'] = None

        info_products['Цена'] = link.find('p',{'data-marker':'item-price'}).text
        s.append(info_products)
    with open('ProductsAvito.json', 'w', encoding='UTF-8') as file:
        json.dump(s, file,indent=4, ensure_ascii=False)


def get_info(item_name:str = 'Телефон') -> None:
    '''функция принимает запрос от пользователя и начинает суету'''
    t = random.uniform(1, 3)
    options = uc.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    
    options.add_argument('--headless')  # Включаем headless-режим
    options.add_argument('--no-sandbox')  # Отключаем sandbox для повышения стабильности
    options.add_argument('--disable-dev-shm-usage')  # Решает проблемы с памятью в headless-режиме

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    options.add_argument(f'--user-agent={user_agent}')

    driver = uc.Chrome(use_subprocess=False, options=options,version_main=132)
    driver.implicitly_wait(t)

    driver.get(url='https://avito.ru')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'styles-module-input-rA1dB'))
    )
    driver.execute_script("window.scrollBy(0, 10)")
    find_input = driver.find_element(By.CLASS_NAME,'styles-module-input-rA1dB')
    find_input.clear()
    find_input.send_keys(item_name)
    find_input.send_keys(Keys.ENTER)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'styles-module-input-rA1dB'))
    )
    text = str(driver.page_source)
    driver.quit()
    
    parser(text)
    

def main():
    get_info()

if __name__ =='__main__':
    main()
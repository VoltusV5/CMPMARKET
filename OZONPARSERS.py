#Парсер для озона который сохраняет всю информацию о первых 12+- выпавших продуктов в json файл
#Он не запуститься если у вас не установлен драйвер на хром
#Пизда время час ночи я дописал!!!!!
import json
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def colleсt_product_info(driver, url:str ='') -> dict:
    '''Функция которая ищет всю информацию про товары(кроме ссылки на товар)'''

    driver.switch_to.new_window('tab')

    time.sleep(0.5)
    driver.get(url=url)
    time.sleep(0.5)

    product_id = driver.find_element(By.XPATH, '//div[contains(text(), "Артикул: ")]'
    ).text.split('Артикул: ')[1]                                                                    # Поиск артикула
    
    page_sourse = str(driver.page_source)
    soup = BeautifulSoup(page_sourse, 'lxml')

    with open(f'product.html', 'w', encoding='UTF-8') as file:                                      #Сохранение HTML кода страницы с товаром ВОЗМОЖНО это поможет ускорить поиск
        file.write(page_sourse)
    
    product_name = soup.find("div", {'data-widget':'webProductHeading'}).find(                      #Поиск названия
        'h1').text.strip().replace('\t','').replace('\n',' ')
    
    product_photo = soup.find('div', {'data-widget':'webGallery'}).find('img')['src']               #Поиск картинки
    
    product_time = ''

    try:                                                                                            
        product_stat = soup.find(
        'div',{"data-widget": "webSingleProductScore"}).find().text.strip()                         #В этом блоке происходит поиск отзывово и звёзд 
        
        if " • " in product_stat:
            product_stars = product_stat.split(" • ")[0].strip()
            product_reviews = product_stat.split(" • ")[1].strip()
        else:
            product_stat = product_stat
    except:
        product_stat = None
        product_stars = None
        product_reviews = None

    try:
        ozon_card_price_element = soup.find(                                                         
            'span', string="c Ozon Картой").parent.find('div').find('span')                         #Проверяем наличие цены с озон картой
        product_ozon_card_price = ozon_card_price_element.text.strip(
        ) if ozon_card_price_element else ''

        price_element = soup.find(
            'span', string="без Ozon Карты").parent.parent.find('div').findAll('span')

        product_discount_price = price_element[0].text.strip(
        ) if price_element[0] else ''
        product_base_price = price_element[1].text.strip(
        ) if price_element[1] is not None else ''
    except:
        product_ozon_card_price = None
        product_discount_price = None
        product_base_price = None

    # product price
    try:
        ozon_card_price_element = soup.find(
            'span', string="c Ozon Картой").parent.find('div').find('span')
    except AttributeError:                                                              #Если в предыдущем блоке нету цены с озон картой то тут найдуться остальные цены +-
        card_price_div = soup.find(
            'div', attrs={"data-widget": "webPrice"}).findAll('span')
        try:
            product_base_price = card_price_div[0].text.strip()
            product_discount_price = card_price_div[1].text.strip()
        except:
            product_discount_price = None
    
    product_data = (
        {
            'product_id': product_id,                                #Артикул
            'product_name': product_name,                            
            'product_ozon_card_price': product_ozon_card_price,      #Цена по карте озон
            'product_discount_price': product_discount_price,        #Цена со скидкой
            'product_base_price': product_base_price,                #Цена без скидок и без озон карты
            'product_statistic': product_stat,                       #Полная статистика товара, количество звёзд + колво отзывов
            'product_stars': product_stars,                          #Только количество звёзд
            'product_reviews': product_reviews,                      #Только количество отзывов с самим словом(Пример: 275 отзывов)
            'product_photo': product_photo,
            'pruduct_url': url,
        }
    )

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return product_data




def get_products_links(item_name:str = 'наушники ') -> None:
    '''функция принимает запрос от пользователя и начинает суету'''
    driver = uc.Chrome()
    driver.implicitly_wait(3)

    driver.get(url='https://ozon.ru')
    time.sleep(1)

    find_input = driver.find_element(By.NAME, 'text')
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(1)

    find_input.send_keys(Keys.ENTER)
    time.sleep(1)

    current_url = f'{driver.current_url}&sorting=rating'
    driver.get(url=current_url)
    time.sleep(1)

    page_sourse = str(driver.page_source)
    soup = BeautifulSoup(page_sourse, 'lxml')
    products_url = list(set([f'https://ozon.ru{i["href"]}' for i in soup.find_all('a', class_='tile-clickable-element')]))          #поиск ссылок

    products_data = []
    for url in  products_url:
        data = colleсt_product_info(driver, url)
        time.sleep(0.3)
        products_data.append(data)

    with open('PRODUCTS_DATA.json', 'w', encoding='UTF-8') as file:
        json.dump(products_data,file,indent=4,ensure_ascii=False)
    
    driver.close()
    driver.quit()

def main():
    get_products_links()

if __name__=='__main__':
    main()
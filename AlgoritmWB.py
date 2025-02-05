from datetime import datetime, timedelta
import dateparser
import json

def k_rating(rating: int):
    if rating < 4.0:
        return 0.1
    elif 4.0 <= rating < 4.3:
        return 0.2
    elif 4.3 <= rating < 4.5:
        return 0.35
    elif 4.5 <= rating < 4.6:
        return 0.5
    elif 4.6 <= rating < 4.7:
        return 0.7
    elif 4.7 <= rating < 4.8:
        return 0.8
    elif 4.8 <= rating <= 5.0:
        return 1.0

def k_feedback(feedback):
    if feedback < 10:
        return 0.07
    elif 10 <= feedback < 20:
        return 0.13
    elif 20 <= feedback < 30:
        return 0.22
    elif 30 <= feedback < 50:
        return 0.37
    elif 50 <= feedback < 100:
        return 0.52
    elif 100 <= feedback < 300:
        return 0.70
    elif 300 <= feedback < 500:
        return 0.85
    elif feedback >= 500:
        return 1.0


def get_days_until_date(date_string):
    today = datetime.now()
    
    try:
        parsed_date = dateparser.parse(date_string)
    except Exception as e:
        return None
    
    if not isinstance(parsed_date, datetime):
        return None
    
    delta = parsed_date - today
    days_until_date = delta.days
    
    return days_until_date


def k_time(product_time: str):
    month = {
        'марта':'March', 
        'апреля':'April',
        'мая':'May',
        'июня':'June', 
        'июля':'July',
        'августа':'August',
        'сентября':'September',
        'октября':'October',
        'ноября':'November',
        'декабря':'December',
        'февраля':'February',
        }
    try:
        if ' ' in product_time:
            product_time = product_time.replace(product_time[product_time.find(' ')+1:], month[product_time[product_time.find(' ')+1:].lower()])
    except:
        return 0.35
    

    if get_days_until_date(product_time) == 1:
        return 1.0
    elif get_days_until_date(product_time) == 2:
        return 0.9
    elif 3 <= get_days_until_date(product_time) <= 4:
        return 0.75
    elif 5 <= get_days_until_date(product_time) <= 7:
        return 0.55
    elif 8 <= get_days_until_date(product_time) <= 11:
        return 0.35
    elif 12 <= get_days_until_date(product_time) <= 21:
        return 0.26
    elif 22 <= get_days_until_date(product_time) <= 30:
        return 0.1
    elif get_days_until_date(product_time) > 30:
        return 0.05


def min_price(products_info:list[dict]) -> int:
    return int(min(products_info, key=lambda x: int(x['Цена'].replace('₽','').replace('\xa0','')))['Цена'].replace('₽','').replace('\xa0',''))

def max_price(products_info:list[dict]) -> int:
    return int(max(products_info, key=lambda x: int(x['Цена'].replace('₽','').replace('\xa0','')))['Цена'].replace('₽','').replace('\xa0',''))

def average_value(products_info:list[dict]) -> float:
    k = 0
    for i in products_info:
        k += int(i['Цена'].replace('₽','').replace('\xa0',''))
    return k/len(products_info)

def k_price(min_ : int, average : float|int, max_ : int, price:int) -> float:
    
    if price == min_:
        return 1.0
    elif min_ < price <= average:
        return round(1.0 - (price - min_) / (average - min_) * 0.4,2)  # Постепенное снижение до 0.6
    elif average < price <= max_:
        return round(0.6 - (price - average) / (max_ - average) * 0.5, 2)  # Стремительное падение до 0.1
    elif price > max_:
        return 0.1


def sorting_products(products: list[dict]) -> list:
    min_ = min_price(products)
    max_ = max_price(products)
    average = average_value(products)
    weight = []
    for item in products:
        try:
            rating = k_rating(float(item['Звёзды'].replace(',','.')))
        except:
            rating = 0
        try:
            feedback = k_feedback(int(item['Оценки'].replace('\xa0','').replace(item['Оценки'][item['Оценки'].find('о'):], '')))
        except:
            feedback = 1.0
        time = k_time(item['Время'])
        price = k_price(min_, average,max_, int(item['Цена'].replace('₽','').replace('\xa0','')))
        weight.append(round(rating+feedback+time+price, 2))
    return weight


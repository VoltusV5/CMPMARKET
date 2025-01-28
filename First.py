import json
from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time
from curl_cffi import requests

def init_webdriver():
    driver = webdriver.Chrome()
    stealth(
        driver,
        platform="win32",
        webgl_vendor="intel inc.",
        renderer='intel Iris OpengGL Engine'
    )
    driver.maximize_window()
    return driver

def scrolldown(driver, deep: int) -> None:
    for _ in range(deep):
        driver.execute_script('window.scrollBy(0,500)')
        time.sleep(0.1)


def get_product_info(product_url: str) -> tuple[str]:
    session = requests.Session()

    raw_data = session.get("https://www.ozon.ru/api/composer-api.bx/page/json/v2?url=" + product_url)
    print(raw_data.content)
    return 0
    # json_data = json.loads(raw_data.content.decode())

    # full_name = json_data["seo"]["title"]

    # if json_data["layout"][0]["component"] == "userAdultModal":
    #     product_id = str(full_name.split()[-1])[1:-1]
    #     print(product_id, full_name)
    #     return (product_id, full_name, "Товар для лиц старше 18 лет", None, None)
    # else:
    #     description = json.loads(json_data["seo"]["script"][0]["innerHTML"])["description"]
    #     image_url = json.loads(json_data["seo"]["script"][0]["innerHTML"])["image"]
    #     price = json.loads(json_data["seo"]["script"][0]["innerHTML"])["offers"]["price"] + " " +\
    #             json.loads(json_data["seo"]["script"][0]["innerHTML"])["offers"]["priceCurrency"]
    #     rating = json.loads(json_data["seo"]["script"][0]["innerHTML"]["ratingValue"])
    #     rating_counter = json.loads(json_data["seo"]["script"][0]["innerHTML"]["reviewCount"])
    #     product_id = json.loads(json_data["seo"]["script"][0]["innerHTML"])["sku"]

    #     return (product_id, full_name, description, price, rating, rating_counter, image_url)
    
def get_mainpage_cards(driver, url):
    driver.get(url)
    scrolldown(driver, 50)
    main_page_html = BeautifulSoup(driver.page_source, "lxml")

    content = main_page_html.find("div", {"class": "container"})
    content = content.findChildren(recursive=False)[-1].find("div")
    content = content.findChildren(recursive=False)
    content = [item for item in content if "island" in str(item)][-1]
    content = content.find("div").find("div").find("div")
    content = content.findChildren(recursive=False)
    
    all_cards = []
    for layer in content:
        layer = layer.find("div")
        cards = layer.findChildren(recursive=False)
        for card in cards:
            card = card.findChildren(recursive=False)
            
            card_name = card[2].find("span", {"class":"tsBody500Medium"}).contents[0]
            card_url = card[2].find("a", href=True)["href"]
            product_url = "https://ozon.ru" + card_url
            
            product_id, full_name, description, price, rating, rating_counter, image_url = get_product_info(card_url)
            card_info = {product_id: {"short_name": card_name,
                                      "full_name": full_name,
                                      "description": description,
                                      "url": product_url,
                                      "rating": rating,
                                      "rating_counter": rating_counter,
                                      "price": price,
                                      "image_url": image_url
                                      }
                         }
            print(card_info)
            all_cards.append(card_info)
            print(product_id, "- DONE")

if __name__=="__main__":
    driver = init_webdriver()
    get_mainpage_cards(driver, "https://ozon.ru")
    driver.quit()
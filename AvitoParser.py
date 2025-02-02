from urllib.parse import quote
from bs4 import BeautifulSoup
import requests
                                    # &s=104 - по дате
                                    # &s=1 - дешевле
                                    # 
item = "телефон"
a = f'https://www.avito.ru/sankt-peterburg?q={quote(item)}'
status = requests.get("https://www.avito.ru/sankt-peterburg?q=%D0%A2%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD")
print(status.status_code)
print(a) #https://www.avito.ru/sankt-peterburg?q=%D0%A2%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD
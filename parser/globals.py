import undetected_chromedriver as uc
options = uc.ChromeOptions()
options.add_argument('--blink-settings=imagesEnabled=false')
    
options.add_argument('--headless')  # Включаем headless-режим
options.add_argument('--no-sandbox')  # Отключаем sandbox для повышения стабильности
options.add_argument('--disable-dev-shm-usage')  # Решает проблемы с памятью в headless-режиме

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
options.add_argument(f'--user-agent={user_agent}')

driver = uc.Chrome(use_subprocess=False,options=options, version_main=132)
driver.implicitly_wait(1)
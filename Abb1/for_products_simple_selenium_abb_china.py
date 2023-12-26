import time
import json
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException

chromeOptions = Options()
driver = webdriver.Chrome(executable_path=r'abb\chromedriver.exe', options=chromeOptions)

prods = []

with open('abb\category.json', 'r') as f:
    urls = json.load(f)

for url in urls:
    driver.get(url['category'])
    time.sleep(5)
    tprod = driver.find_elements(By.XPATH, '//div[@class="goods-info"]//a')
    for element in tprod:
        prods.append(element.get_attribute('href'))
    try:
        while driver.find_element(By.XPATH, '//div[@class="mini-pageview"]//span[@class="page-action"]//a[@class="flip next"]'):
            # clickable = driver.find_element(By.XPATH, '//div[@class="mini-pageview"]//span[@class="page-action"]//a[@class="flip next"]')
            driver.execute_script("document.querySelector('span.page-action').querySelector('a.next').click();")
            # clickable.click()
            time.sleep(5)
            tprod = driver.execute_script("return Array.from(document.querySelectorAll('div.goods-info a')).map(a => a.getAttribute('href'));")
            prods.extend(tprod)
            print('interation success')
            print(len(prods))
    except:
        print("no more new page")

# tprod = driver.find_elements(By.XPATH, '//div[@class="goods-info"]//a')
#         for element in tprod:
#             prods.append(element.get_attribute('href'))
with open('product_abb_china_25may2023.json', 'w') as f:
    json.dump(prods, f)

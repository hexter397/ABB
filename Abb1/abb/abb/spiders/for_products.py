import scrapy
import json
from scrapy_selenium import SeleniumRequest 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class ForProductsSpider(scrapy.Spider):
    name = "for_products"
    base_url = 'https://mall.abb.com.cn'
    def start_requests(self):
        with open('../product_abb_china_25may2023.json', 'r') as f:
            urls = json.load(f)
        try:
            for url in urls:
                yield {'url' : url}
        except:
            for url in urls:
                yield {'url' : self.base_url + url}

    # def parse(self, response):
    #     yield{
    #         'product' : response.url
    #     }
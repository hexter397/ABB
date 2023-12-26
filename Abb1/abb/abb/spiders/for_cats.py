import scrapy
import json
from scrapy_selenium import SeleniumRequest 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class ForCatsSpider(scrapy.Spider):
    name = "for_cats"
    base_url = 'https://mall.abb.com.cn'
    def start_requests(self):
        yield SeleniumRequest(
            url= 'https://mall.abb.com.cn/index.php',
            callback= self.parse,
            wait_time=5
        )

    def parse(self, response):
        for cat in response.xpath('//div[@class="cat-root-box"]/a/@href').getall():
            yield {
                'category' : self.base_url + cat
            }

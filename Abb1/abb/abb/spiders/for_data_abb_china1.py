import scrapy
import json
from ..utils import translate_new
from ..utils import clean
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import codecs
class ChinaSpider(scrapy.Spider):
    name = "for_data"
    crawled_urls = []

    def start_requests(self):
        with codecs.open('./data.json', 'r', encoding='utf-8') as f:
            crawled_data = json.load(f)
        
        for c_data in crawled_data:
            c_url = c_data['Product_url']
            self.crawled_urls.append(c_url)

        with open('./products_abb_china_25may2023.json', 'r') as f:
            urls = json.load(f)

        for lnk in urls:
            if lnk["product_link"] not in self.crawled_urls:
                print("*************************************************************")
                print(lnk["product_link"])
                print("*************************************************************")
                self.crawled_urls.append(lnk["product_link"])
                yield SeleniumRequest(
                    url=lnk["product_link"],
                    callback=self.parse,
                    wait_time=10
                )
            else:
                print("*************************************************************")
                print("Already Crawled")
                print("*************************************************************")

    def parse(self, response):
        item = {}
        item['Product_url'] = response.url
        item['Product_name'] = self.parse_product_name(response)
        item['Product_price'] = self.parse_product_price(response)
        item['part_number1'] = translate_new(response.xpath('(//div[@class="other-infos-item"]//span[not(contains(@class, "product-infos-tit"))]//text())[1]').get())
        item['part_number2'] = translate_new(response.xpath('(//div[@class="other-infos-item"]//span[not(contains(@class, "product-infos-tit"))]//text())[2]').get())
        item['product_specifications'] = self.parse_product_specifications(response)
        item['Bread_Crumbs'] = self.parse_bread_crumbs(response)
        item['web_Series_link'] = self.parse_web_series_links(response)
        item['Primary_image'] = self.parse_primary_image(response)
        item['Secondary_images'] = self.parse_secondary_images(response)
        item['Product_Brand_Name'] = self.parse_brand_name(response)
        item['Product_description'] = self.parse_product_description(response)
        item['Product_meta_data'] = self.parse_meta_data(response)
        item['Product_extra_data'] = self.parse_product_extra_data(response)
        yield item

    def parse_product_extra_data(self, response):
        value = translate_new(response.xpath('//div[@class="other-infos-item"]//span[not(contains(@class, "product-infos-tit"))]//text()').getall())
        key = translate_new(response.xpath('//div[@class="other-infos-item"]//span[contains(@class, "product-infos-tit")]//text()').getall())

        if len(value) == 9:
            item = dict(zip(key, value))
        else:
            if 'Product Description:' in key:
                index = key.index('Product Description:')
                key.pop(index)
            item = dict(zip(key, value))
        return item

    def parse_product_description(self, response):
        item = self.parse_product_specifications(response).get("Product Description:", "")
        return clean(translate_new(item))
    
    def parse_product_name(self, response):
        item = response.xpath('//div[@class="product-titles"]/h2//text()').get()
        return clean(translate_new(item))

    def parse_product_price(self, response):
        item = response.xpath('//div[@class="product-concerns goods-price-tag"]//b[@class="price"]//text()').get()
        return clean(translate_new(item))

    def parse_product_specifications(self, response):
        key = translate_new(response.xpath('//div[@id="more_props"]//table//tr/td[1]//text()').getall())
        value = translate_new(response.xpath('//div[@id="more_props"]//table//tr/td[2]//text()').getall())
        item = dict(zip(key , value))
        return item

    def parse_bread_crumbs(self, response):
        item = clean(translate_new(response.xpath('//div[@class="bread-crumbs"]//a//text()').getall()))
        return item
       
    def parse_web_series_links(self, response):
        item_keys = clean(translate_new(response.xpath('//div[@class="bread-crumbs"]//a//text()').getall()))
        item_values = response.xpath('//div[@class="bread-crumbs"]//a/@href').getall()

        for i, value in enumerate(item_values):
            if '/index.php/' in value:
                index = value.index('/index.php/')
                modified_value = "https://mall.abb.com.cn" + value
                item_values[i] = modified_value
            elif '#' in value:
                index = value.index('#')
                modified_value = response.url
                item_values[i] = modified_value
            else:
                pass
        
        item = dict(zip(item_keys, item_values))
        return item

    def parse_brand_name(self, response):
        item = clean(translate_new(response.xpath('(//div[@class="product-attributes"]//li/a/text())[1]').get()))
        return item

    def parse_primary_image(self, response):
        item = response.xpath('//div[@id="product_album"]//div[@class="product-album-pic"]//img/@src').get()
        return item

    def parse_secondary_images(self, response):
        item = response.xpath('//div[@class="thumbnail-list"]//li[not(contains(@class,"active"))]//img/@src').getall()
        return item

    def parse_meta_data(self, response):
        item = {
            'keyword': response.xpath('//meta[@name="keywords"]/@content').get(),
            'description': response.xpath('//meta[@name="description"]/@content').get(),
            'title' : response.xpath('//meta[@name="title"]/@content').get()
        }
        return item

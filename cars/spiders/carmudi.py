#Scrapy Python
#Finished @ Friday, November 4th 2016 13.30 WIB
#Created by : Hendi Santika
#Waslap / Telegram : +6281321411881
#Skype : hendi.santika 

import scrapy
import MySQLdb
import re
from tld import get_tld
from string import Template

class Tes1(scrapy.Spider):
    name = "carmudi"
    start_urls = [
        'http://www.carmudi.co.id/cars/',
    ]

    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "root", "root", "olx")
        self.stmt = "insert into cars(url, title, price, posted, city, province, contact_person, description, source_site, year, transmission, brand, model, type, ownership, nego, uploaded_by, phone, seen) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def parse(self, response):
        urls = response.xpath('//section[contains(@class, "catalog-listing")]//h5[contains(@class, "item-title")]/a/@href').extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_cars)
            yield request

        # process next page
        # next_page_url = response.xpath('//*[@id="body-container"]/div/div/div/span/a/@href').extract_first()
        # next_page_url = response.xpath('//*[@id="body-container"]/div/div/div[2]/span[16]/a/@href').extract_first() # YANG INI UNTUK NGETES DOANG
        current_page = int(response.xpath('//ul[contains(@class,"pagination")]/li[@class="current"]/a/text()').extract_first())
        last_page = int(response.xpath('//ul[contains(@class,"pagination")]/li[last()]/a/text()').extract_first())
        next_page_url = '?page=%d' % (current_page+1 if current_page < last_page else None,)
        if next_page_url is None:
            return

        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_cars(self, response):
        c = self.db.cursor()
        title = response.xpath('//div[@class="title-bar"]/span/text()').extract_first().strip()
        price_tmp = response.xpath('//div[contains(@class, "car-value")]/output/text()').extract_first().strip()
        price = re.sub('[Rp. ]', "", price_tmp)
        city = ''
        province = ' '.join(response.xpath('//div[@id="addressBlock"]/address/text()').extract()).strip()
        posted = response.xpath('//p[@class="submitted"]/span[1]/text()').extract_first().strip()
        cp = response.xpath('//p[contains(@class, "dealer-name")]/strong/text()').extract_first()
        desc = ''
        ss = get_tld(response.url)
        year = ''
        transmission = ''
        brand = ''
        model = ''
        tipe = ''
        ownership = ''
        nego = ''
        uploaded_by = ''
        phone = ''
        seen = ''

        cars = {
            'url'           : response.url,
            'title'         : title,
            'price'         : price,
            'city'          : city,
            'province'      : province,
            'posted'        : posted,
            'cp'            : cp,
            'desc'          : desc,
            'url'           : response.url,
            'source_site'   : ss,    
            'transmission'  : transmission,
            'brand'         : brand,
            'model'         : model,    
            'type'          : tipe,   
            'year'          : year,   
            'ownership'     : ownership,
            'nego'          : nego,    
            'uploaded_by'   : uploaded_by,   
            'phone'         : phone,   
            'seen'          : seen   
            }
        yield cars                 



 

              


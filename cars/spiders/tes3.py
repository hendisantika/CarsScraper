# -*- coding: utf-8 -*-
import scrapy
import MySQLdb


class TripadvisorSpider(scrapy.Spider):
    name = 'tes3'
    allowed_domains = ['olx.co.id']
    start_urls = (
        'http://olx.co.id/mobil/',
    )

    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "root", "root", "olx")
        self.stmt = "insert into cars(url, title, price, posted, city) values(%s, %s, %s, %s, %s)"

    def parse(self, response):
        # c = self.db.cursor()
        # process each restaurant link
        urls = response.xpath('//table[@id="offers_table"]/tbody/tr/td/table/tbody/tr/td[3]/h3/a/@href').extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_cars)
        
        # title = response.xpath(
        #     '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/h1/text()').extract_first()
        # price = response.xpath(
        #     '//*[@id="offeractions"]/div/div/div[1]/strong/text()').extract_first()
        # city = response.xpath(
        #     '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/span[1]/span[2]/strong/a/text()').extract_first()
        # posted = response.xpath(
        #     '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/small/span/text()').extract_first()
        # url2 = response.url
        
        # c.execute("insert into cars(url, title, price, posted, city) values(%s, %s, %s, %s, %s)", (url2, title, price, posted, city))
        # self.db.commit()  
        yield request

        # process next page
        next_page_url = response.xpath('//*[@id="body-container"]/div/div/div/span/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_cars(self, response):
        # c = self.db.cursor()
        title = response.xpath(
            '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/h1/text()').extract_first().strip()
        price = response.xpath(
            '//*[@id="offeractions"]/div/div/div[1]/strong/text()').extract_first()
        city = response.xpath(
            '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/span[1]/span[2]/strong/a/text()').extract_first()
        posted = response.xpath(
            '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/small/span/text()').extract_first().strip()
        # url = response.url
        cars = {
            'title': title,
            'price': price,
            'city': city,
            'posted': posted,
            'url': response.url}
            # 'url': url}
        # c.execute("insert into cars(url, title, price, posted, city) values(%s, %s, %s, %s, %s)", (url, title, price, posted, city))
        # self.db.commit()    
        yield cars
        
    
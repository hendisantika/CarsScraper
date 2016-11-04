# -*- coding: utf-8 -*-
import scrapy
import MySQLdb


class Tes5Spider(scrapy.Spider):
    name = 'tes5'
    allowed_domains = ['olx.co.id']
    start_urls = (
        'http://olx.co.id/mobil/',
    )


    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "root", "root", "olx")
        self.stmt = "insert into cars(url, title, price, posted, city, contact_person) values(%s, %s, %s, %s, %s, %s)"

    def parse(self, response):
        c = self.db.cursor()
        # process each restaurant link
        # urls = response.xpath('//table[@id="offers_table"]/tbody/tr/td/table/tbody/tr/td[3]/h3/a/@href').extract()
        urls = response.xpath('//table[@id="offers_table"]/tbody/tr/td/table/tbody/tr/td[3]/h3/a/@href').extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_cars)
            yield request

        # process next page
        # next_page_url = response.xpath('//*[@id="body-container"]/div/div/div/span/a/@href').extract_first()
        next_page_url = response.xpath('//*[@id="body-container"]/div/div/div[2]/span[2]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

        #tambahan
        # if next_page_url:
        #     absolute_next_page_url = response.urljoin(next_page_url)
        #     yield scrapy.Request(absolute_next_page_url, callback=self.parse_contractors)


    def parse_cars(self, response):
        # title = response.xpath(
        #     '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/h1/text()').extract_first().strip()
        # price = response.xpath(
        #     '//*[@id="offeractions"]/div/div/div[1]/strong/text()').extract_first()
        # city = response.xpath(
        #     '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/span[1]/span[2]/strong/a/text()').extract_first()
        # posted = response.xpath(
        #     '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/small/span/text()').extract_first().strip()
        # cp = response.xpath(
        #     '//*[@id="offeractions"]/div/div/div[3]/div/p/span[1]/text()').extract_first().strip()
        # desc = response.xpath(
        #     '//*[@id="textContent"]/p/text()').extract_first().strip()
        title = response.xpath(
            '//*[@id="offer_active"]/div/div/div/div/h1/text()').extract_first().strip()
        price = response.xpath(
            '//*[@id="offeractions"]/div/div/div/strong/text()').extract_first().strip()
        city = response.xpath(
            '//*[@id="offer_active"]/div/div/div/div/p/span/span/strong/a/text()').extract_first()
        posted = response.xpath(
            '//*[@id="offer_active"]/div/div/div/div/p/small/span/text()').extract_first().strip()
        cp = response.xpath(
            '//*[@id="offeractions"]/div/div/div/div/p/span/text()').extract_first().strip()
        desc = response.xpath(
            '//*[@id="textContent"]/p/text()').extract_first().strip()


        
        cars = {
            'title': title,
            'price': price,
            'city': city,
            'posted': posted,
            'cp'    : cp,
            'desc'  : desc,
            'url': response.url}
            # 'url': url}
        yield cars
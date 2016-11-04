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
    name = "olx"
    start_urls = [
        'http://olx.co.id/mobil/bekas/',
    ]

    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "root", "root", "olx")
        self.stmt = "insert into cars(url, title, price, posted, city, province, contact_person, description, source_site, year, merek, model, type, old_new, nego, uploaded_by, phone, seen) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def parse(self, response):
        urls = response.xpath('//table[@id="offers_table"]/tbody/tr/td/table/tbody/tr/td[3]/h3/a/@href').extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_cars)
            yield request

        # process next page
        # next_page_url = response.xpath('//*[@id="body-container"]/div/div/div/span/a/@href').extract_first()
        next_page_url = response.xpath('//*[@id="body-container"]/div/div/div[2]/span[16]/a/@href').extract_first() # YANG INI UNTUK NGETES DOANG
        # next_page_url = response.xpath('//*[@id="body-container"]/div/div/div/span[@class="fbold next abs large"]/a/@href').extract_first() #YANG INI UDAH OK NEXT PAGE NYA NICH
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_cars(self, response):
        c = self.db.cursor()
        title = response.xpath(
            '//*[@id="offer_active"]/div/div/div/div/h1/text()').extract_first().strip()
        price_tmp = response.xpath(
            '//*[@id="offeractions"]/div/div/div/strong/text()').extract_first().strip()
        price = re.sub('[Rp. ]', "", price_tmp)
        city_tmp1 = response.xpath(
            '//*[@id="offer_active"]/div/div/div/div/p/span/span/strong/a/text()').extract_first()
        city_tmp2 = city_tmp1.split(",")
        city = city_tmp2[0].strip()
        province = city_tmp2[1].strip()
        posted_tmp = response.xpath(
            # '//*[@id="offer_active"]/div/div/div/div/p/small/span/text()').extract_first().strip()
            '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/small/span/text()').extract_first().strip()
        posted = posted_tmp
        # b = {'Ditambahkan': '', 'sejak': '', ',' : '', '  ' : ' '}
        # Pattern untuk tanggal posting
        # b = {'Ditambahkan': '', 'sejak': '', ',' : '', '  ' : ' '}
        # for x,y in b.items():
        #     posted = posted.replace(x, y).strip()
           

        cp = response.xpath(
            '//*[@id="offeractions"]/div/div/div/div/p/span/text()').extract_first().strip()
        desc = response.xpath(
            '//*[@id="textContent"]/p/text()').extract_first().strip()
        ss = get_tld(response.url)
        year = response.xpath(
                    '//*[@id="offerdescription"]/div[2]/div[1]/ul/li[3]/a/text()').extract_first().strip()
        merek = ''
        model = response.xpath(
                    '//*[@id="offerdescription"]/div[2]/div[1]/ul/li[1]/a/text()').extract_first().strip()
        tipe = ''
        old_new = 'Bekas'
        nego = response.xpath(
                    '//*[@id="offeractions"]/div/div/div[1]/small/text()').extract_first().strip()
        uploaded_by = response.xpath(
                        '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/small/span/a/span/text()').extract_first().strip()
        phone = ''
        seen = response.xpath(
                        '//*[@id="offerbottombar"]/div[3]/strong/text()').extract_first().strip()



        # c.execute("insert into cars(url, title, price, posted, city, province, contact_person, description, source_site, year, merek, model, type, old_new, nego, uploaded_by, phone, seen) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
        #          (response.url, title, price, posted, city, province, cp, desc, ss, year, merek, model, tipe, old_new, nego, uploaded_by, phone, seen))
        # self.db.commit()    

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
            'merek'         : merek,
            'model'         : model,    
            'type'          : tipe,   
            'year'          : year,   
            'old'           : old_new,
            'nego'          : nego,    
            'uploaded_by'   : uploaded_by,   
            'phone'         : phone,   
            'seen'          : seen   
            }
        yield cars                 



 

              


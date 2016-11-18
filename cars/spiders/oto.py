#Scrapy Python
#Finished @ Friday, November 4th 2016 13.30 WIB
#Created by : Hendi Santika
#Waslap / Telegram : +6281321411881
#Skype : hendi.santika 

import scrapy
import MySQLdb
import re
from tld import get_tld
import time
import os

class Oto(scrapy.Spider):
    name = "oto"
    start_urls = [
        'http://oto.my/search/?pg=1',
    ]

    def __init__(self):
        #self.db = MySQLdb.connect("127.0.0.1", "root", "root", "olx")
        #self.stmt = "insert into jualo_cars(url, title, city, province, description, price, contact_person, source_site, year, brand,  model, type, ownership, engine_capacity, engine_type, transmission, doors, color, airbags, gps, radio, cd_player,  posted, nego, uploaded_by, phone, seen) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        pass

    def parse(self, response):
        #urls = response.xpath('//*[@id="http://www.mudah.my/2006+Naza+Ria+2+5+A+-50009385.htm"]/ul/li[2]/div/div[1]/div[1]/h2/a/@href').extract()
        # urls = response.xpath('//*[contains(@class, "list_ads")]/ul/li[@class="listing_ads_params"]/div/div/div/h2/a/@href').extract()
        # urls = response.xpath('//div[@class="results-container list-view"]').extract()
        urls = response.xpath('//div[@class="results-container list-view"]/div/div/a/@href').extract()

        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_cars)
            yield request
            # time.sleep(2)

        # process next page
        # next_page_url = response.xpath('//*[@id="classified-listings-result"]/div[9]/ul/li[6]/a/@href').extract_first() #YANG INI BUAT NGETES DOANG
        next_page_url = response.xpath('//*[@id="page-container"]/div[3]/div/div/div[1]/div[2]/div/div[2]/div[1]/ul/li[7]/a/@href').extract_first() #YANG INI BUAT NGETES DOANG
        # next_page_url = response.xpath('//a[@class="next_page"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_cars(self, response):
        #c = self.db.cursor()
        # title = response.xpath('//html/body/div/div/table/tbody/tr/td/div[@class="ad_show_title"]/text()').extract_first()
        title = response.xpath('//*[@id="page-container"]/div[5]/div/div/div/div[1]/div[2]/text()').extract_first().strip()
        
        city = '\n'.join(response.xpath('//*[@id="page-container"]/div[5]/div/div/div/div[1]/div[3]/text()').extract()).strip()
        #city_tmp2 = filter(None, re.split("[-]+", city_tmp1))
        # city_tmp2 = re.findall(r"[\w']+", city_tmp1)
        #city = city_tmp2[0].strip()
        #province = city_tmp2[1].strip() + ", " + city_tmp2[2].strip()
        # city, province = city_tmp1.split("-")
        province = city
        
        # desc = '\n'.join(response.xpath('//*[@id="page-container"]/div[5]/div/div/div/div[1]/div[8]/text()').extract()).strip().replace('<br>', '\n')
        # desc = " ".join(response.xpath('//*[@id="page-container"]/div[5]/div/div/div/div[1]/div[8]/text()').extract()).strip()
        desc = '\n'.join(response.xpath('//*[@id="page-container"]/div[5]/div/div/div/div[1]/div[8]/text()').extract()).strip()
        # desc = desc.rstrip(desc.linesep)
        desc = re.sub('[\r\n]', " ", desc)
        # desc = desc.replace('\n', ' ').replace('\r', '')
        # desc = desc.strip()
        
        #price_tmp = response.xpath('//div[@class="real_price"]/text()').extract_first().strip()
        #price = re.sub('[Rp. ]', "", price_tmp)
        price = response.xpath('//*[@id="page-container"]/div[5]/div/div/div/div[1]/div[1]/text').extract_first() 
         # ' + response.xpath('//dd[@class="dd-price"]/meta[@itemprop="price"]/@content').extract_first()

        # cp = response.xpath('//html/body/div/div/table/tbody/tr/td/table/tbody/tr/td/div/div/div/div/a/text()').extract_first()
        cp = response.xpath('//*[@id="page-container"]/div[5]/div/div/div/div[2]/div[1]/div[2]/div[1]/text()').extract_first()
        cp = cp.strip() if cp is not None else ''
        # print "contact person : ", cp
        
        ss = get_tld(response.url)
        year = response.xpath('//*[@id="page-container"]/div[5]/div/div/div/div[1]/div[7]/div/div[1]/ul/li[5]/div[2]/text').extract_first()
        brand = response.xpath('//*[@id="page-container"]/div[5]/div/div/div/div[1]/div[7]/div/div[1]/ul/li[1]/div[2]/a/text').extract_first()
        model = response.xpath('//*[@id="page-container"]/div[5]/div/div/div/div[1]/div[7]/div/div[1]/ul/li[2]/div[2]/a/text()').extract_first()
        model = model.strip() if model is not None else '' 
        tipe = response.xpath('//*[@id="page-container"]/div[5]/div/div/div/div[1]/div[7]/div/div[1]/ul/li[3]/div[2]/text()').extract_first()
                    #'/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/div[2]/table/tbody/tr/td[1]/div/text()').extract_first()
        tipe = tipe.strip() if tipe is not None else ''
        # print "tipe : ", tipe
        
        ownership = '\n'.join(response.xpath('//*[@id="page-container"]/div[5]/div/div/div/div[1]/div[7]/div/div[1]/ul/li[4]/div[2]/text()').extract()).strip()
        if ownership == "Bekas" : ownership = 'used'
        else : ownership = 'new'
        # print "ownership : ", ownership
        engine_capacity = response.xpath('//*[@id="listing_2912099"]/div[2]/div[2]/div[5]/div/p[5]/span[2]/text()').extract_first()
        engine_type = response.xpath('//*[@id="listing_2912099"]/div[3]/div[1]/div/div[2]/div/div[2]/div[2]/div/div[3]/div[11]/div/p/span[2]/text()').extract_first()
        transmission = response.xpath('//*[@id="listing_2912099"]/div[2]/div[2]/div[5]/div/p[6]/span[2]/text()').extract_first()
        # print "transmission : ", transmission

        doors = response.xpath('//*[@id="listing_2912099"]/div[3]/div[1]/div/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/div/p/span[2]/text()').extract_first()
        color = response.xpath('//*[@id="listing_2912099"]/div[2]/div[2]/div[5]/div/p[6]/span[2]/text()').extract_first()
        airbags = ''
        gps = ''
        radio = ''
        cd_player = ''
        posted = '\n'.join(response.xpath('//*[@id="listing_2912099"]/div[2]/div[1]/div[1]/div/div[1]/div[2]/text()').extract()).strip()
        nego = ''
        uploaded_by = ''
        phone = ''      
        #seen = response.xpath('//*[@id="view_count"]/text()').extract_first().strip()

        # c.execute("insert into jualo_cars(url, title, city, province, description, price, contact_person, source_site, year, brand,  model, type, ownership, engine_capacity, engine_type, transmission, doors, color, airbags, gps, radio, cd_player,  posted, nego, uploaded_by, phone, seen) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
        #          (response.url, title, city, province, desc, price, cp, ss,  year, model, tipe, ownership, engine_capacity, engine_type, transmission, doors, color, airbags, gps, radio, cd_player, posted, nego, uploaded_by, phone, seen)
        # self.db.commit()   

        # print "Title : ", title 

        cars = {
            'url'           : response.url,
            'title'         : title,
            'city'          : city,
            'province'      : province,
            'description'   : desc,
            'price'         : price,
            'cp'            : cp,
            'source_site'   : ss, 
            'year'          : year, 
            'brand'         : brand,
            'model'         : model,   
            'type'          : tipe,  
            'ownership'     : ownership,
            'engine_capacity': engine_capacity,
            'engine_type'   : engine_type,
            'transmission'  : transmission,
            'doors'         : doors,
            'color'         : color,
            'airbags'       : airbags,
            'gps'           : gps,
            'radio'         : radio,
            'cd_player'     : cd_player,
            'posted'        : posted,
            'nego'          : nego,
            'uploaded_by'   : uploaded_by,
            'phone'         : phone,
            #'seen'          : seen 
            }
        yield cars                 

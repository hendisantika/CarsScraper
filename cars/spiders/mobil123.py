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
import time

class Tes1(scrapy.Spider):
    name = "mobil123"
    start_urls = [
        'http://www.mobil123.com/mobil?type=used'
    ]

    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "root", "root", "olx")
        self.stmt = "insert into cars_test2(url, title, price, posted, city, province, source_site, year, transmission, brand, model, type, ownership, engine_capacity, doors) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def parse(self, response):
        # urls = response.xpath('//*[@id="listing_3232491"]/div/div[2]/h2/a/@href').extract()
        urls = response.xpath('//article[contains(@class, "listing")]/div/div[2]/h2/a/@href').extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_cars)
            yield request
            time.sleep(2)

        # process next page
        next2 = 'http://www.mobil123.com/'
        next_page_url = response.xpath('//*[@id="classified-listings-result"]/div[6]/ul/li[6]/a/@href').extract_first() #YANG INI UDAH OK NEXT PAGE NYA NICH
        # next_page_url = response.xpath('//*[@id="body-container"]/div/div/div[2]/span[16]/a/@href').extract_first() # YANG INI UNTUK NGETES DOANG 
        # next_page_url = response.xpath('//*[@id="classified-listings-result"]/div[6]/ul/li[6]/a/@href').extract_first() # YANG INI UNTUK NGETES DOANG 
        # next_page_url = response.xpath('//article[contains(@class,"listing")]/div[6]/ul/li[6]/a/@href').extract_first() # YANG INI UNTUK NGETES DOANG 
        # next_page_url = response.xpath('//*[@id="classified-listings-result"]/div[6]/ul/li[6]/a/@href').extract_first() # YANG INI UNTUK NGETES DOANG 
        


        absolute_next_page_url = response.urljoin(next_page_url)
        # Supaya gak kena rate limits
        time.sleep(2)
        request = scrapy.Request(absolute_next_page_url)
        print"next url : ", absolute_next_page_url
        yield request

    def parse_cars(self, response):
        c = self.db.cursor()
        title = ' '.join(response.xpath('//article[contains(@class,"listing")]/div[2]/div[1]/div[1]/div/div[1]/h1/a/text()').extract()).strip()
        # price_tmp = response.xpath('//article[contains(@class,"listing")]/div[2]/div[1]/div[1]/div/div[2]/p[2]/text()').extract_first()
        # price_tmp = response.xpath('//*[@id="listing_3232491"]/div[2]/div[1]/div[1]/div/div[2]/p[@class="listing__price delta flush"]').extract_first()
        price_tmp = response.xpath('//article[contains(@class,"listing--details")]/div[2]/div/div/div/div[2]/p[contains(@class,"listing__price")]/text()').extract_first().strip()
        # price_tmp = response.xpath('//*[@id="listing_3232491"]/div[2]/div[1]/div[1]/div/div[2]/p[2]/text()').extract_first()
        # price_tmp = price_tmp.strip() if price_tmp is not None else 'Hai Sayang' 
        price = re.sub('[Rp. ]', "", price_tmp)
        # price = price_tmp
        city_tmp1 = response.xpath('//article[contains(@class,"listing")]/div[2]/div[2]/div[1]/div/div/div[2]/text()').extract_first().strip()
        city_tmp1 = city_tmp1.replace(u'\xbb', '|')
        # string.replace(u'\xbb', u'&raquo;')
        # city = response.xpath('//article[contains(@class,"listing")]/div[2]/div[2]/div[1]/div/div/div[2]/text()').extract_first().strip()
        # city = response.xpath('//article[contains(@class,"listing")]/div[2]/div[2]/div[1]/div/div/div[2]/text()').extract_first()
        # province = response.xpath('//article[contains(@class,"listing")]/div[2]/div[2]/div[1]/div/div/div[2]/text()').extract_first().strip()
        # city_tmp2 = city_tmp1.split("\>>")
        # city_tmp2 = city_tmp1.split("\xbb")
        # city_tmp2 = re.split("[>]+", city_tmp1)
        # city_tmp2 = filter(None, re.split("[>]+", city_tmp1))
        city_tmp2 = filter(None, re.split("[|]+", city_tmp1))
        # city_tmp2 = re.findall(r"[\w']+", city_tmp1)
        city = city_tmp2[1].strip()
        province = city_tmp2[0].strip()
        # city = city_tmp2[1]
        # province = city_tmp2[0]
        # print "city :", city_tmp2[1], "| province " ,city_tmp2[0]
        # print "city :", city_tmp2
        # posted_tmp = map(unicode.strip, response.xpath('//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/small/span/text()').extract_first())
        # posted_tmp = response.xpath('//*[@id="offer_active"]/div/div/div/div/p/small/span/text()').extract()
        # posted_tmp = response.xpath('//*[@id="offer_active"]/div/div/div/div/p/small/span/text()').extract()
        # posted_tmp = response.xpath('//*[@id="offer_active"]/div/div/div/div/p/small/span/text()').extract()
        posted_tmp = (' '.join(map(unicode.strip, response.xpath('//article[contains(@class,"listing")]/div[2]/div[1]/div[1]/div/div[1]/div[2]/text()').extract())))
        # posted_tmp = response.xpath('normalize-space(//*[@id="offer_active"]/div/div/div/div/p/small/span/text()').extract()
            # '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/small/span/text()').extract_first().strip()
        # posted = posted_tmp
        # posted = re.sub('sejak,', "", posted_tmp)
        posted_tmp = filter(None, re.split("[:]+", posted_tmp)) 
        posted = posted_tmp[1]
        posted = posted.strip() 
        # b = {'sejak ': '', ',' : '', '  ' : ' '}
        # Pattern untuk tanggal posting
        # b = {'Ditambahkan': '', 'sejak': '', ',' : '', '  ' : ' '}
        # for x,y in b.items():
        #     posted = posted.replace(x, y).strip()

        # cp = ''
        # cp = response.xpath('//*[@id="listing_3232491"]/div[2]/div[2]/div[1]/div/div/div[1]/text()').extract_first().strip()
        cp = response.xpath('//article[contains(@class,"listing")]/div[2]/div[2]/div[1]/div/div/div[1]/text()').extract_first().strip()
        desc = ''
        # desc = response.xpath(
        #     '//*[@id="textContent"]/p/text()').extract_first().strip()
        ss = get_tld(response.url)
        # year = response.xpath('//*[@id="listing_3232491"]/div[2]/div[2]/div[5]/div/p[4]/span[2]/text()').extract_first().strip()
        year = response.xpath('//article[contains(@class,"listing")]/div[2]/div[2]/div[5]/div/p[4]/span[2]/text()').extract_first()
        # transmission = response.xpath('//*[@id="listing_3232491"]/div[2]/div[2]/div[5]/div/p[6]/span[2]/text()').extract_first().strip()
        transmission = response.xpath('//article[contains(@class,"listing")]/div[2]/div[2]/div[5]/div/p[6]/span[2]/text()').extract_first()
        # brand = response.xpath('//*[@id="listing_3232491"]/div[2]/div[2]/div[5]/div/p[1]/span[2]').extract_first().strip()
        brand = response.xpath('//article[contains(@class,"listing")]/div[2]/div[2]/div[5]/div/p[1]/span[@class = "float--right"]/text()').extract_first()
        # model = response.xpath('//*[@id="listing_3232491"]/div[2]/div[2]/div[5]/div/p[2]/span[2]/text()').extract_first().strip()
        model = response.xpath('//article[contains(@class,"listing")]/div[2]/div[2]/div[5]/div/p[2]/span[2]/text()').extract_first()
        # tipe = response.xpath('//*[@id="listing_3232491"]/div[2]/div[2]/div[5]/div/p[3]/span[@class = "float--right"]/text()').extract_first()
        # tipe = (''.join(response.xpath('//article[contains(@class,"listing")]/div[2]/div[2]/div[5]/div/p[3]/span/text()').extract_first()))
        tipe = (''.join(response.xpath('//article[contains(@class,"listing")]/div[2]/div[2]/div[5]/div/p[3]/span[2]/text()').extract()))
        # tipe = tipe.strip()
        ownership = 'Used'
        nego = ''
        # eCap = response.xpath('//*[@id="listing_3232491"]/div[2]/div[2]/div[5]/div/p[5]/span[2]/text()').extract_first().strip()
        eCap = response.xpath('//article[contains(@class,"listing")]/div[2]/div[2]/div[5]/div/p[5]/span[2]/text()').extract_first()
        eCap = re.sub('[c ]', "", eCap)
        eType = ''
        # color = response.xpath('//*[@id="listing_3232491"]/div[2]/div[2]/div[5]/div/p[10]/span[2]/text()').extract_first().strip()
        color = response.xpath('//article[contains(@class,"listing")]/div[2]/div[2]/div[5]/div/p[10]/span[2]/text()').extract_first()
        # doors = response.xpath('//*[@id="listing_3232491"]/div[3]/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div[1]/div/p/span[2]/text()').extract_first()
        doors = response.xpath('//article[contains(@class,"listing")]/div[3]/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div[1]/div/p/span[2]/text()').extract_first().strip()
        uploaded_by = ''
        # uploaded_by = response.xpath(
        #                 '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/small/span/a/span/text()').extract_first().strip()
        phone = ''
        seen = ''
        # seen = response.xpath(
        #                 '//*[@id="offerbottombar"]/div[3]/strong/text()').extract_first().strip()


        # print("url :", response.url)
        # print("title :", title)
        # print("Posted2 ", posted2)
        # print("Posted3 ", posted3)
        # print("doors : ",  doors)

        c.execute("insert into cars_test2(url, title, price, posted, city, province, source_site, year, transmission, brand, model, type, ownership, engine_capacity, doors) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                 (response.url, title, price, posted, city, province, ss, year, transmission, brand, model, tipe, ownership, eCap, doors))
        # time.sleep(1)
        self.db.commit()    

        cars = {
            'url'           : response.url,
            'title'         : title,
            'price'         : price,
            'city'          : city,
            'province'      : province,
            'posted'        : posted,
            # 'cp'            : cp,
            # 'desc'          : desc,
            'url'           : response.url,
            'source_site'   : ss,    
            'transmission'  : transmission,
            'brand'         : brand,
            'model'         : model,    
            'type'          : tipe,   
            'year'          : year,   
            'ownership'     : ownership,
            # 'nego'          : nego,    
            'eCap'          : eCap,    
            'doors'         : doors,   
            # 'phone'         : phone,   
            'color'         : color   
            }
        yield cars                 



 

              


#Scrapy Python
#Finished @ Friday, November 4th 2016 13.30 WIB
#Created by : Hendi Santika
#Email : hendisantika@gmail.com
#Waslap / Telegram : +6281321411881
#Skype : hendi.santika

import datetime
import re
# import time
# from datetime import date, datetime, timedelta
import datetime

import scrapy
import MySQLdb
import re
from tld import get_tld

class Tes1(scrapy.Spider):
    name = "jualo"
    start_urls = [
        'https://www.jualo.com/mobil-baru-dan-bekas',
    ]

    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "root", "root", "olx")
        self.stmt = "insert into jualo_cars(url, title, city, province, description, price, contact_person, source_site, year, brand,  model, type, ownership, engine_capacity, engine_type, transmission, doors, color, airbags, gps, radio, cd_player,  posted, nego, uploaded_by, phone, seen) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def parse(self, response):
        urls = response.xpath('/html/body/div[2]/div/div[4]/div[2]/div/div/ul/li/div/div/a/@href').extract()

        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_cars)
            yield request

        # process next page
        # next_page_url = response.xpath('/html/body/div[2]/div/div[4]/div[3]/div[1]/div[@class="pagination"]/a[@class="next_page"]/@href').extract_first() #UDAH OK NICH NEXT PAGE NYA
        next_page_url = response.xpath('/html/body/div[2]/div/div[4]/div[3]/div[1]/div/a[8]/@href').extract_first() #YANG INI BUAT NGETES DOANG
        # next_page_url = response.xpath('//a[@class="next_page"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_cars(self, response):
        c = self.db.cursor()
        # title = response.xpath('//html/body/div/div/table/tbody/tr/td/div[@class="ad_show_title"]/text()').extract_first()
        # title = response.xpath('//html/body/div/div/table/tbody/tr/td[@class="left_ad_show_main_table"]/div[@class="ad_show_title"]/text()').extract_first()
        title = response.xpath('/html/body/div[3]/div/div[3]/div[1]/div[1]/h1/text()').extract_first()
        
        # city_tmp1 = '\n'.join(response.xpath('//td[@class="top_location"]/text()').extract()).strip() // Udah ganti CSS lagi euuy
        city_tmp1 = '\n'.join(response.xpath('//li[@class="top_location"]/text()').extract()).strip()
        city_tmp2 = filter(None, re.split("[,]+", city_tmp1))
        # city_tmp2 = re.findall(r"[\w']+", city_tmp1)
        # city = city_tmp2[0].strip() + ", " + city_tmp2[1].strip()
        # city = city_tmp2[0] + ", " + city_tmp2[1]
        city = city_tmp2[0].strip()
        province = city_tmp2[1].strip() + ", " + city_tmp2[2].strip()
        # province =  city_tmp2[2].strip()
        # province = city_tmp2[2]

        desc = '\n'.join(response.xpath('//div[@class="ad_show_detail"]/text()').extract()).strip().replace('<br>', '\n')
            #'/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/text()').extract_first()    
        
        price = response.xpath('//div[@class="real_price"]/h2/text()').extract_first()
        # price_tmp = response.xpath('/html/body/div[3]/div/div[3]/div[2]/div[2]/div[1]/div/div/h2/text()').extract_first().strip()
        # price = '\n'.join(response.xpath('/html/body/div[3]/div/div[3]/div[2]/div[2]/div[1]/div/div/text()').extract_first().strip())
        price = re.sub('[Rp. ]', "", price)


        # cp = response.xpath('//html/body/div/div/table/tbody/tr/td/table/tbody/tr/td/div/div/div/div/a/text()').extract_first()
        cp = response.xpath('/html/body/div[3]/div/table/tbody/tr/td[2]/table/tbody/tr[4]/td/div/div[2]/div[@class="col-md-12"]/div[@class="col-md-12 name-user"]/a/text()').extract_first()
        cp = cp.strip() if cp is not None else ''
        # print "contact person : ", cp
        
        ss = get_tld(response.url)
        year = ''
        brand = ''
        model = response.xpath('/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/div[2]/table/tbody/tr/td[1]/div/text()').extract_first()
                    #'/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/div[2]/table/tbody/tr/td[1]/div/text()').extract_first()
        model = model.strip() if model is not None else '' 
        # tipe = response.xpath('/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/div[2]/table/tbody/tr/td[1]/div[@class="variant_td"]/text()').extract_first()
        # tipe = response.xpath('/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/div[2]/table/tbody/tr/td[1]/div/text()').extract_first()
        # tipe = response.xpath('/html/body/div[3]/div/div[3]/div[1]/div[5]/div[2]/table/tbody/tr/td[1]/div[@class="variant_td"]/text()').extract_first()
        tipe = response.xpath('/html/body/div[3]/div/div[3]/div[1]/div[5]/div[2]/table/tbody/tr/td[1]/div/text()').extract_first()
        # tipe = tipe.strip() if tipe is not None else ''
        # print "tipe : ", tipe
        
        ownership = '\n'.join(response.xpath('//td[@class="second-hand"]/text()').extract()).strip()
        if ownership == "Bekas" : ownership = 'used'
        else : ownership = 'new'
        # print "ownership : ", ownership
        engine_capacity = ''
        engine_type = ''
        # transmission = response.xpath('/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/div[2]/table/tbody/tr/td[2]/div/text()').extract_first()
        transmission = response.xpath('/html/body/div[3]/div/div[3]/div[1]/div[5]/div[2]/table/tbody/tr/td[2]/div/text()').extract_first()
        # print "transmission : ", transmission

        doors = ''
        color = ''
        airbags = ''
        gps = ''
        radio = ''
        cd_player = ''
        # posted = '\n'.join(response.xpath('//td[@class="top_timer"]/text()').extract()).strip()
        posted_tmp = '\n'.join(response.xpath('//li[@class="top_timer"]/text()').extract()).strip()

        print "Asalnya --> " + posted_tmp
        posted_tmp = filter(None, re.split(" ", posted_tmp))

        if "menit" in posted_tmp:
            a1 = posted_tmp[0]
            posted = datetime.datetime.now() - datetime.timedelta(minutes=int(a1))
        if "jam" in posted_tmp:
            a1 = posted_tmp[0]
            posted = datetime.datetime.now() - datetime.timedelta(hours=int(a1))
        if "hari" in posted_tmp:
            a1 = posted_tmp[0]
            posted = datetime.datetime.now() - datetime.timedelta(days=int(a1))

        nego = ''
        uploaded_by = ''
        phone = ''      
        seen = response.xpath('//*[@id="view_count"]/text()').extract_first().strip()

        print "price -->" + price + " posted --> " + str(posted)
        # print "city : ", city
        # print "province : ", province

        c.execute("insert into jualo_cars(url, title, city, province, description, price, contact_person, source_site, year, brand,  model, type, ownership, engine_capacity, engine_type, transmission, doors, color, airbags, gps, radio, cd_player,  posted, nego, uploaded_by, phone, seen) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                 (response.url, title, city, province, desc, price, cp, ss,  year, brand, model, tipe, ownership, engine_capacity, engine_type, transmission, doors, color, airbags, gps, radio, cd_player, posted, nego, uploaded_by, phone, seen))
        # self.db.commit()

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
            'seen'          : seen 
            }
        # yield cars

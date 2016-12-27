#Scrapy Python
#Finished @ Friday, November 4th 2016 13.30 WIB
#Modified Everyday Since Tuesday, December 13 2016
#Created by : Hendi Santika
#Waslap / Telegram : +6281321411881
#Skype : hendi.santika 

import datetime
import re
from datetime import datetime

import MySQLdb
import scrapy
from tld import get_tld


class Mudah(scrapy.Spider):
    name = "carlist"
    start_urls = [
        'http://www.carlist.my/car',
    ]

    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "root", "root", "scrapyDB")
        self.stmt = "insert into cars(url, title, city, province, description, price, contact_person, source_site, year, brand,  model, type, ownership, engine_capacity, engine_type, transmission, doors, color, airbags, gps, radio, cd_player,  posted, nego, uploaded_by, phone, seen) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # pass

    def parse(self, response):
        #urls = response.xpath('//*[@id="http://www.mudah.my/2006+Naza+Ria+2+5+A+-50009385.htm"]/ul/li[2]/div/div[1]/div[1]/h2/a/@href').extract()
        # urls = response.xpath('//*[contains(@class, "list_ads")]/ul/li[@class="listing_ads_params"]/div/div/div/h2/a/@href').extract()
        urls = response.xpath('//h2[contains(@class, "listing__title")]/a/@href').extract()

        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_cars)
            yield request
            # time.sleep(2)

        # process next page
        # next_page_url = response.xpath('//*[@id="classified-listings-result"]/div[9]/ul/li[6]/a/@href').extract_first() #YANG INI BUAT NGETES DOANG
        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first() #YANG INI UDAH OK NICH
        # next_page_url = response.xpath('//*[@id="classified-listings-result"]/div[9]/ul/li[6]/a/@href').extract_first()
        # next_page_url = response.xpath('//a[@class="next_page"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_cars(self, response):
        c = self.db.cursor()
        # title = response.xpath('//html/body/div/div/table/tbody/tr/td/div[@class="ad_show_title"]/text()').extract_first()
        #title = response.xpath('//*[@id="listing_2912099"]/div[2]/div[1]/div[1]/div/div[1]/h1/a/text()').extract_first()
        title = response.xpath('//h1[contains(@class, "article__title")]/a/text()').extract_first()
        
        #city = '\n'.join(response.xpath('//*[@id="listing_2912099"]/div[2]/div[2]/div[1]/div/div/div[2]/text()').extract()).strip()
        city = response.xpath('//i[contains(@class, "icon--location")]/../text()').extract_first().strip()
        #city_tmp2 = filter(None, re.split("[-]+", city_tmp1))
        # city_tmp2 = re.findall(r"[\w']+", city_tmp1)
        #city = city_tmp2[0].strip()
        #province = city_tmp2[1].strip() + ", " + city_tmp2[2].strip()
        # city, province = city_tmp1.split("-")
        province = city
        
        #desc = '\n'.join(response.xpath('//div[@class="ad_show_detail"]/text()').extract()).strip().replace('<br>', '\n')
            #'/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/text()').extract_first()    
        desc = '\n'.join(response.xpath('//span[@itemprop="description"]/text()').extract())
        # desc = desc.strip()
        desc = re.sub('[\n\t]', " ", desc)
        desc = desc.strip()
        #price_tmp = response.xpath('//div[@class="real_price"]/text()').extract_first().strip()
        #price = re.sub('[Rp. ]', "", price_tmp)
        #price = response.xpath('//*[@id="listing_2912099"]/div[2]/div[1]/div[1]/div/div[2]/p[2]/text').extract_first() 
        price = response.xpath('(//p[contains(@class, "listing__price")])[1]/text()').extract_first()
        price = re.sub('[RM, ]', "", price)
         # ' + response.xpath('//dd[@class="dd-price"]/meta[@itemprop="price"]/@content').extract_first()

        # cp = response.xpath('//html/body/div/div/table/tbody/tr/td/table/tbody/tr/td/div/div/div/div/a/text()').extract_first()
        cp = response.xpath('/html/body/div[3]/div/table/tbody/tr/td[2]/table/tbody/tr[4]/td/div/div[2]/div[@class="col-md-12"]/div[@class="col-md-12 name-user"]/a/text()').extract_first()
        cp = cp.strip() if cp is not None else ''
        # print "contact person : ", cp
        
        ss = get_tld(response.url)
        year = response.xpath('//span[text()="Year"]/following-sibling::span/text()').extract_first()
        brand = response.xpath('//span[text()="Make"]/following-sibling::span/text()').extract_first()
        model = response.xpath('//span[text()="Model"]/following-sibling::span/text()').extract_first()
        model = model.strip() if model is not None else '' 
        tipe = response.xpath('//span[text()="Variant"]/following-sibling::span/text()').extract_first()
                    #'/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/div[2]/table/tbody/tr/td[1]/div/text()').extract_first()
        tipe = tipe.strip() if tipe is not None else ''

        ownership = '\n'.join(response.xpath('///*[@id="listing_2912099"]/div[2]/div[2]/div[5]/div/p[9]/span[2]/text()').extract()).strip()
        if ownership == "Bekas" : ownership = 'used'
        else : ownership = 'new'
        # print "ownership : ", ownership
        engine_capacity = response.xpath('//span[text()="Engine Capacity"]/following-sibling::span/text()').extract_first()
        engine_capacity = re.sub('[cc ]', "", engine_capacity)
        engine_type = response.xpath('//span[text()="Engine Type"]/following-sibling::span/text()').extract_first()
        transmission = response.xpath('//span[text()="Transmission"]/following-sibling::span/text()').extract_first()
        # print "transmission : ", transmission

        doors = response.xpath('//span[text()="Doors"]/following-sibling::span/text()').extract_first()
        color = response.xpath('//span[text()="Colour"]/following-sibling::span/text()').extract_first()
        airbags = ''
        satnav = ''
        radio = ''
        cd_player = ''
        #posted = '\n'.join(response.xpath('//*[@id="listing_2912099"]/div[2]/div[1]/div[1]/div/div[1]/div[2]/text()').extract()).strip()
        posted = response.xpath('//div[contains(@class, "listing__updated")]/text()').extract_first().split(':')[1].strip()
        data = filter(None, re.split(" ", posted))
        tgl1 = data[1].replace(',', '')
        bln1 = data[0]
        thn1 = data[2]
        posted = datetime.strptime(tgl1 + " " + bln1 + " " + thn1, '%d %B %Y')

        nego = ''
        uploaded_by = ''
        phone = ''  
        # seen =''    
        #seen = response.xpath('//*[@id="view_count"]/text()').extract_first().strip()

        c.execute("insert into cars(url, title, city, province, description, price, contact_person, source_site, year, "
                  "brand,  model, type, ownership, engine_capacity, engine_type, transmission, doors, color, airbags, "
                  "satnav, radio, cd_player,  posted, nego, uploaded_by, phone) "
                  "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                 (response.url, title, city, province, desc, price, cp, ss,  year, brand, model, tipe, ownership,
                  engine_capacity, engine_type, transmission, doors, color, airbags, satnav, radio, cd_player, posted, nego, uploaded_by, phone))
        self.db.commit()

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
            'satnav'        : satnav,
            'radio'         : radio,
            'cd_player'     : cd_player,
            'posted'        : posted,
            'nego'          : nego,
            'uploaded_by'   : uploaded_by,
            'phone'         : phone,
            # 'seen'          : seen 
            }
        yield cars

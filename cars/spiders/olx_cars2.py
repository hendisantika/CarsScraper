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
import datetime
from datetime import datetime
from datetime import date


class Tes1(scrapy.Spider):
    name = "olx2"
    start_urls = [
        'http://olx.co.id/mobil/bekas/',
    ]

    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "root", "root", "olx")
        self.stmt = "insert into cars_tes3(url, title, price, posted, city, province, contact_person, description, source_site, year, transmission, brand, model, type, ownership, nego, uploaded_by, phone, seen) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def parse(self, response):
        urls = response.xpath('//table[@id="offers_table"]/tbody/tr/td/table/tbody/tr/td[3]/h3/a/@href').extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_cars)
            yield request

        # process next page
        # next_page_url = response.xpath('//*[@id="body-container"]/div/div/div/span/a/@href').extract_first()
        # next_page_url = response.xpath('//*[@id="body-container"]/div/div/div[2]/span[16]/a/@href').extract_first() # YANG INI UNTUK NGETES DOANG
        next_page_url = response.xpath('//*[@id="body-container"]/div/div/div/span[@class="fbold next abs large"]/a/@href').extract_first() #YANG INI UDAH OK NEXT PAGE NYA NICH
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_cars(self, response):
        tahun = date.today().year
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
        # posted_tmp = map(unicode.strip, response.xpath('//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/small/span/text()').extract_first())
        # posted_tmp = response.xpath('//*[@id="offer_active"]/div/div/div/div/p/small/span/text()').extract()
        # posted_tmp = response.xpath('//*[@id="offer_active"]/div/div/div/div/p/small/span/text()').extract()
        # posted_tmp = response.xpath('//*[@id="offer_active"]/div/div/div/div/p/small/span/text()').extract()
        posted_tmp = (' '.join(map(unicode.strip, response.xpath('//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/small/span/text()').extract()))).strip()
        # posted_tmp = response.xpath('normalize-space(//*[@id="offer_active"]/div/div/div/div/p/small/span/text()').extract()
            # '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/small/span/text()').extract_first().strip()
        # posted = posted_tmp
        # posted = re.sub('sejak,', "", posted_tmp)
        posted = posted_tmp 
        b = {'sejak ': '', ',' : '', '  ' : ' '}
        # Pattern untuk tanggal posting
        # b = {'Ditambahkan': '', 'sejak': '', ',' : '', '  ' : ' '}
        for x,y in b.items():
            posted = posted.replace(x, y).strip()

        if ":" in posted:
           tgl = time.strftime("%Y-%m-%d")
           posted = tgl +" "+ posted
        elif " " in posted:
            mon = dict(jan='Jan',
                       feb='Feb',
                       peb='Feb',
                       mar='Mar',
                       apr='Apr',
                       mei='May',
                       jun='Jun',
                       jul='Jul',
                       ags='Ags',
                       sep='Sep',
                       okt='Oct',
                       nov='Nov',
                       nop='Nov',
                       des='Dec')
            posted = filter(None, re.split(" ", posted))
            tgl = posted[0]
            bln = posted[1]

            if any(x in posted[1] for x in mon.keys()):
                bln = mon.get(posted[1].lower(), 'Tidak ada')
            posted = datetime.strptime(tgl +" " + bln +" " + str(tahun), '%d %b %Y')
        elif "kemarin" in posted:
            posted = date.today() - timedelta(1)
        else:
            posted = time.strftime("%Y-%m-%d %H:%M:%S")

        cp = response.xpath(
            '//*[@id="offeractions"]/div/div/div/div/p/span/text()').extract_first().strip()
        desc = response.xpath(
            '//*[@id="textContent"]/p/text()').extract_first().strip()
        ss = get_tld(response.url)
        year = response.xpath(
                    '//*[@id="offerdescription"]/div[2]/div[1]/ul/li[3]/a/text()').extract_first().strip()
        transmission = response.xpath(
                    '//*[@id="offerdescription"]/div[2]/div[1]/ul/li[2]/a/text()').extract_first().strip()
        brand = ''
        model = response.xpath(
                    '//*[@id="offerdescription"]/div[2]/div[1]/ul/li[1]/a/text()').extract_first().strip()
        tipe = ''
        ownership = 'Used'
        nego = response.xpath(
                    '//*[@id="offeractions"]/div/div/div[1]/small/text()').extract_first().strip()
        uploaded_by = response.xpath(
                        '//*[@id="offer_active"]/div[3]/div[1]/div[1]/div[1]/p/small/span/a/span/text()').extract_first().strip()
        phone = ''
        seen = response.xpath(
                        '//*[@id="offerbottombar"]/div[3]/strong/text()').extract_first().strip()


        c.execute("insert into cars_tes3(url, title, price, posted, city, province, contact_person, description, source_site, year, transmission, brand, model, type, ownership, nego, uploaded_by, phone, seen) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                 (response.url, title, price, posted, city, province, cp, desc, ss, year, transmission, brand, model, tipe, ownership, nego, uploaded_by, phone, seen))
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


    def convert(posted):
        tahun = date.today().year
        # posted = str
        if ":" in posted:
           tgl = time.strftime("%Y-%m-%d")
           posted = tgl +" "+ posted
        elif " " in posted:
            #mon = ['Jan', 'jan', 'feb', 'Feb', 'peb', 'Peb', 'Mar', 'mar', 'Apr', 'apr', 'Mei', 'mei', 'Jun', 'jun', 'Jul', 'jul', 'Ags', 'ags', 'Sep', 'sep', 'Okt', 'okt', 'Nop','nop', 'Des', 'des']
            mon = dict(jan='Jan',
                       feb='Feb',
                       peb='Feb',
                       mar='Mar',
                       apr='Apr',
                       mei='May',
                       jun='Jun',
                       jul='Jul',
                       ags='Ags',
                       sep='Sep',
                       okt='Oct',
                       nov='Nov',
                       nop='Nov',
                       des='Dec')
            # posted = "2 Okt"
            posted = filter(None, re.split(" ", posted))
            tgl = posted[0]
            bln = posted[1]

            if any(x in posted[1] for x in mon.keys()):
                bln = mon.get(posted[1].lower(), 'Tidak ada')
                #if "Jan" in posted[1]:
                #    bln = "Jan"
                #elif "jan" in posted[1]:
                #    bln = "jan"
                #if "Feb" in posted[1]:
                #    bln = "Feb"
                #elif "feb" in posted[1]:
                #    bln = "feb"
                #elif "Peb" in posted[1]:
                #    bln = "Feb"
                #elif "peb" in posted[1]:
                #    bln = "feb"
                #elif "Mar" in posted[1]:
                #    bln = "mar"
                #elif "mar" in posted[1]:
                #    bln = "mar"
                #elif "Apr" in posted[1]:
                #    bln = "Apr"
                #elif "apr" in posted[1]:
                #    bln = "apr"
                #elif "Mei" in posted[1]:
                #    bln = "May"
                #elif "mei" in posted[1]:
                #    bln = "may"
                #elif "Jun" in posted[1]:
                #    bln = "Jun"
                #elif "jun" in posted[1]:
                #    bln = "jun"
                #elif "Jul" in posted[1]:
                #    bln = "Jul"
                #elif "jul" in posted[1]:
                #    bln = "jul"
                #elif "Ags" in posted[1]:
                #    bln = "aug"
                #elif "ags" in posted[1]:
                #    bln = "aug"
                #elif "Sep" in posted[1]:
                #    bln = "Sep"
                #elif "sep" in posted[1]:
                #    bln = "sep"
                #elif "Okt" in posted[1]:
                #    bln = "Oct"
                #elif "okt" in posted[1]:
                #    bln = "oct"
                #elif "Nop" in posted[1]:
                #    bln = "Nov"
                #elif "nop" in posted[1]:
                #    bln = "nov"
                #elif "Des" in posted[1]:
                #    bln = "Dec"
                #elif "des" in posted[1]:
                #    bln = "dec"
                #else: print "Gak ada"

            posted = datetime.strptime(tgl +" " + bln +" " + str(tahun), '%d %b %Y')
        elif "kemarin" in posted:
            posted = date.today() - timedelta(1)
        else:
            posted = time.strftime("%Y-%m-%d %H:%M:%S")
        return posted




 

              


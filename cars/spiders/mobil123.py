#UDAH OKE UNTUK INSERT INTO MYSQL DB NYA MAH
#TINGGAL NEXT PAGE

import scrapy
import MySQLdb
import re
from tld import get_tld

class Tes1(scrapy.Spider):
    name = "mobil123"
    start_urls = [
        'http://www.mobil123.com/mobil?type=used',
    ]

    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "root", "root", "olx")
        self.stmt = "insert into cars(url, title, price, posted, city, province, contact_person, description, source_site, year, merek, type, old_new) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def parse(self, response):
        urls = response.xpath('//*[@id="listing_3232491"]/div/div[2]/h2/a').extract()

        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_cars)
            yield request

        # process next page
        # next_page_url = response.xpath('/html/body/div[2]/div/div[4]/div[3]/div[1]/div/a[@class="next_page"]/@href').extract_first() #UDAH OK NICH NEXT PAGE NYA
        #next_page_url = response.xpath('/html/body/div[2]/div/div[4]/div[3]/div[1]/div/a[8]/@href').extract_first() #YANG INI BUAT NGETES DOANG
        next_page_url = response.xpath('//a[@class="next_page"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_cars(self, response):
        c = self.db.cursor()
        title = response.xpath(
            '//*[@id="listing_3232491"]/div[2]/div[1]/div[1]/div/div[1]/h1/a/text()').extract_first()
        price = response.xpath(
            '//*[@id="listing_3232491"]/div[2]/div[1]/div[1]/div/div[2]/p[2]/text()').extract_first().strip()
        # price = re.sub('[Rp. ]', "", price_tmp)
        city = '\n'.join(response.xpath(
            #'/html/body/div[3]/div/table/tbody/tr/td[1]/table[1]/tbody/tr/td[3]/text()').extract_first()
            '//*[@id="listing_3232491"]/div[2]/div[2]/div[1]/div/div/div[2]/text()').extract()).strip()
        posted = '\n'.join(response.xpath(
            #'/html/body/div[3]/div/table/tbody/tr/td[1]/table[1]/tbody/tr/td[2]/text()').extract_first()
            '//*[@id="listing_3232491"]/div[2]/div[1]/div[1]/div/div[1]/div[2]/text()').extract()).strip()
        cp = response.xpath(
            '/html/body/div[3]/div/table/tbody/tr/td[2]/table/tbody/tr[4]/td/div/div[2]/div[1]/div[1]/a/text()').extract_first()
        desc = '\n'.join(response.xpath(
            #'/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/text()').extract_first()
            '//div[@class="ad_show_detail"]/text()').extract()).strip().replace('<br>', '\n')
        ss = get_tld(response.url)
        year = response.xpath(
                '//*[@id="listing_3232491"]/div[2]/div[2]/div[5]/div/p[4]/span[2]/text()').extract_first()
        tipe = response.xpath(
                    #'/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/div[2]/table/tbody/tr/td[1]/div/text()').extract_first()
                '//td[@class="variant_td"]/text()').extract_first()
        tipe = tipe.strip() if tipe is not None else ''
        old_new = '\n'.join(response.xpath(
                    #'/html/body/div[3]/div/table/tbody/tr/td[1]/table[1]/tbody/tr/td[1]/text()').extract_first()
                    '//td[@class="second-hand"]/text()').extract()).strip()
        merek = ''

        # c.execute("insert into cars(url, title, price, posted, city, contact_person, description, source_site, year, merek, type, old_new) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
        #          (response.url, title, price, posted, city, cp, desc, ss, year, merek, tipe, old_new))
        # self.db.commit()    

        cars = {
            'title': title,
            'price': price,
            'city': city,
            'posted': posted,
            'cp'    : cp,
            'desc'  : desc,
            'url': response.url,
            'source_site ' : ss,    
            'merek ': merek,   
            'type ' :  tipe,   
            'year ' :  year,   
            'old ' :  old_new   
            }
            # 'url': url}
        yield cars                 

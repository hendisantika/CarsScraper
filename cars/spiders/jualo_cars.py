#UDAH OKE UNTUK INSERT INTO MYSQL DB NYA MAH
#TINGGAL NEXT PAGE

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
        self.stmt = "insert into jualo_cars(url, title, price, posted, city, contact_person, description) values(%s, %s, %s, %s, %s, %s, %s)"

    def parse(self, response):
        urls = response.xpath('/html/body/div[2]/div/div[4]/div[2]/div/div/ul/li/div/div/a/@href').extract()

        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_cars)
            yield request

        # process next page
        # next_page_url = response.xpath('/html/body/div[2]/div/div[4]/div[3]/div[1]/div/a[@class="next_page"]/@href').extract_first() #UDAH OK NICH NEXT PAGE NYA
        next_page_url = response.xpath('/html/body/div[2]/div/div[4]/div[3]/div[1]/div/a[8]/@href').extract_first() #YANG INI BUAT NGETES DOANG
        # next_page_url = response.xpath('//a[@class="next_page"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_cars(self, response):
        c = self.db.cursor()
        title = response.xpath('//html/body/div/div/table/tbody/tr/td/div[@class="ad_show_title"]/text()').extract_first()
        price_tmp = response.xpath('//div[@class="real_price"]/text()').extract_first().strip()
        price = re.sub('[Rp. ]', "", price_tmp)
        city_tmp1 = '\n'.join(response.xpath('//td[@class="top_location"]/text()').extract()).strip()
        city_tmp2 = filter(None, re.split("[,]+", city_tmp1))
        # city_tmp2 = re.findall(r"[\w']+", city_tmp1)
        city = city_tmp2[0].strip()
        province = city_tmp2[1].strip()
            
        posted = '\n'.join(response.xpath('//td[@class="top_timer"]/text()').extract()).strip()
        cp = response.xpath('//html/body/div/div/table/tbody/tr/td/table/tbody/tr/td/div/div/div/div/a/text()').extract_first()
        cp = cp.strip() if cp is not None else ''
        desc = '\n'.join(response.xpath('//div[@class="ad_show_detail"]/text()').extract()).strip().replace('<br>', '\n')
            #'/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/text()').extract_first()
            
        ss = get_tld(response.url)
        year = ''
        model = response.xpath('/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/div[2]/table/tbody/tr/td[1]/div/text()').extract_first()
                    #'/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/div[2]/table/tbody/tr/td[1]/div/text()').extract_first()
                
        model = model.strip() if model is not None else '' 
        tipe = response.xpath('//td[@class="variant_td"]/text()').extract_first()
                    #'/html/body/div[3]/div/table/tbody/tr/td[1]/div[4]/div[2]/table/tbody/tr/td[1]/div/text()').extract_first()
                
        tipe = tipe.strip() if tipe is not None else ''
        ownership = '\n'.join(response.xpath('//td[@class="second-hand"]/text()').extract()).strip()
                    #'/html/body/div[3]/div/table/tbody/tr/td[1]/table[1]/tbody/tr/td[1]/text()').extract_first()
                    
        model = ''

        # c.execute("insert into cars(url, title, price, posted, city, contact_person, description, source_site, year, model, type, old_new) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
        #          (response.url, title, price, posted, city, cp, desc, ss, year, model, tipe, old_new))
        # self.db.commit()    

        cars = {
            'title'         : title,
            'price'         : price,
            'city'          : city,
            'province'      : province,
            'posted'        : posted,
            'cp'            : cp,
            'desc'          : desc,
            'url'           : response.url,
            'source_site'   : ss,    
            'model'         : model,    
            'type'          : tipe,   
            'year'          : year,   
            'ownership'     : ownership,   
            'url'           : response.url
            }
        yield cars                 

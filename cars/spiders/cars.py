import scrapy
import MySQLdb
# import mysql

class carsSpider(scrapy.Spider):
    name = "cars"
    start_urls = [
        'http://olx.co.id/mobil/',
    ]

    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "root", "root", "olx")
        self.stmt = "insert into cars(url, title, price, posted, city) values(%s, %s, %s, %s, %s)"

    def parse(self, response):
                # c = self.db.cursor()
                for items in response.xpath('//table[@id="offers_table"]/tbody/tr/td/table/tbody'):
                # for items in response.xpath('//table[@id="offers_table"]/tbody/tr/td/table/tbody/tr/td/div/p/strong'):
                    # print 'price: ', items.xpath('./tr/td[4]/div/p/strong/text()').extract()
                    # print 'url: ', items.xpath('./tr/td[3]/h3/a/@href').extract()
                    # print 'title: ', items.xpath('./tr/td[3]/h3/a/span/text()').extract()
                    
                    
                    yield {
                        'url': items.xpath('./tr/td/h3/a/@href').extract_first().strip(),
                        'title': items.xpath('./tr/td/h3/a/span/text()').extract_first().strip(),
                        'price': items.xpath('./tr/td/div/p/strong/text()').extract_first().strip(),
                        #'description' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                        #'source' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                        'posted' : items.xpath('./tr/td[1]/p/text()').extract_first().strip(),
                        #'type' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                        'city' : items.xpath('./tr/td/p/small/span/text()').extract_first().strip(),
                        #'area' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                        #'apartment' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                        #'luas' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                        #'certificate' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                        
                    }

                #     title = items.xpath('./tr/td[3]/h3/a/span/text()').extract()[0]
                #     price = items.xpath('./tr/td[4]/div/p/strong/text()').extract()[0]
                #     c.execute("insert into rumah(title, price) values(%s,%s)", (title, price))
                # self.db.commit()

                
                next_page_url = response.xpath('//*[@id="body-container"]/div/div/div/span/a/@href').extract_first()
                if next_page_url is not None:
                    yield scrapy.Request(response.urljoin(next_page_url))




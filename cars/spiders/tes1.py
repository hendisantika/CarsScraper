import scrapy
import MySQLdb

class Tes1(scrapy.Spider):
    name = "tes"
    start_urls = [
        'http://olx.co.id/mobil/',
    ]

    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "root", "root", "olx")
        self.stmt = "insert into cars(url, title, price, posted, city) values(%s, %s, %s, %s, %s)"

    def parse(self, response):
            c = self.db.cursor()
            for items in response.xpath('//table[@id="offers_table"]/tbody/tr/td/table/tbody'):
            # for items in response.xpath('//table[@id="offers_table"]/tbody/tr/td/table/tbody/tr/td/div/p/strong'):
                # print 'price: ', items.xpath('./tr/td[4]/div/p/strong/text()').extract()
                # print 'url: ', items.xpath('./tr/td[3]/h3/a/@href').extract()
                # print 'title: ', items.xpath('./tr/td[3]/h3/a/span/text()').extract()
                
                
                #yield {
                #'url': items.xpath('./tr/td[3]/h3/a/@href').extract(),
                #'title': items.xpath('./tr/td[3]/h3/a/span/text()').extract(),
                #'price': items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                #'description' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                #'sourceSite' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                #'posted' : items.xpath('./tr/td/p/text()').extract(),
                #'type' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                #'city' : items.xpath('./tr/td/p/small/span/text()').extract(),
                #'area' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                #'apartmentName' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                #'luas' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                #'certificate' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                #}

                # title = items.xpath('./tr/td[3]/h3/a/span/text()').extract()[0]
                # price = items.xpath('./tr/td[4]/div/p/strong/text()').extract()[0]
                url =  items.xpath('./tr/td[3]/h3/a/@href').extract()
                title = items.xpath('./tr/td[3]/h3/a/span/text()').extract()
                price = items.xpath('./tr/td[4]/div/p/strong/text()').extract()
                # 'description' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                # 'sourceSite' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                posted = items.xpath('./tr/td/p/text()').extract()
                # 'type' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                city =  items.xpath('./tr/td/p/small/span/text()').extract()
                # 'area' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                # 'apartmentName' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                # 'luas' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),
                # 'certificate' : items.xpath('./tr/td[4]/div/p/strong/text()').extract(),

                # print 'url' + url,
                # print 'title' + title,
                # print 'price' + price,
                # print 'posted' + posted,
                # print 'city' + city
            #     c.execute("insert into cars(url, title, price, posted, city) values(%s, %s, %s, %s, %s)", (url, title, price, posted, city)
            # self.db.commit()

            

              



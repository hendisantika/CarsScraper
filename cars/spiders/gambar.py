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

from pytesseract import image_to_string
# import pytesseract 
# import image_to_string
from PIL import Image
import cStringIO

class Tes1(scrapy.Spider):
    name = "gambar"
    start_urls = [
            'https://storage.jualo.com/user_phones/1655079/phone_number20161114-143-q7vseu.jpg'
    ]

    def __init__(self):
        #self.db = MySQLdb.connect("127.0.0.1", "root", "root", "olx")
        #self.stmt = "insert into cars_test(url, title, price, posted, city, province, source_site, year, transmission, brand, model, type, ownership, engine_capacity, doors) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        pass

    def parse(self, response):
        stream = cStringIO.StringIO(response.body)
        a = image_to_string(Image.open(stream))
        print 'Text: ', a

#!/bin/bash
#Scrapy Python
#Finished @ Thursday, December 14th 2016 19.05 WIB
#Created by : Hendi Santika
#Waslap / Telegram : +6281321411881
#Skype : hendi.santika 
# Activate the ENV for OLX Spider
source ~/Documents/python/ENV/bin/activate
cd /home/hendisantika/Documents/python/cars/cars
scrapy crawl carlist 2>&1 | tee /home/hendisantika/Documents/python/cars/cars/logs/carlist.log


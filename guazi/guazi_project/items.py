# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GuaziProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 车源号
    car_location = scrapy.Field()
    car_brand = scrapy.Field()
    car_id = scrapy.Field()
    car_name = scrapy.Field()
    car_url = scrapy.Field()
    car_price = scrapy.Field()
    car_jr_price = scrapy.Field()
    license_time = scrapy.Field()
    car_meter = scrapy.Field()
    displacement = scrapy.Field()
    transmission_case = scrapy.Field()


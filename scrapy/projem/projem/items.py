# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProjemItem(scrapy.Item):
    # define the fields for your item here like:
    land=scrapy.Field()
    city = scrapy.Field()
    province=scrapy.Field()
    population=scrapy.Field()

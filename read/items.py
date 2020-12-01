# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReadItem(scrapy.Item):
    item_title = scrapy.Field()
    item_author = scrapy.Field()
    item_full_price = scrapy.Field()
    item_discount = scrapy.Field()
    item_link = scrapy.Field()
    item_rating = scrapy.Field()
    _id = scrapy.Field()

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
def big_photo(url):
    if url:
        url = url.replace('w_82,h_82', 'w_2000,h_2000')
    return url



def char_data(value):
    return ''.join(value.split())



class StroyparcerItem(scrapy.Item):

    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(big_photo))
    link = scrapy.Field(output_processor=TakeFirst())
    price_1 = scrapy.Field(input_processor=MapCompose(char_data), output_processor=TakeFirst())
    per_unit = scrapy.Field(output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    left_side = scrapy.Field()
    right_side = scrapy.Field(input_processor=MapCompose(char_data))
    properties = scrapy.Field()
    price = scrapy.Field()

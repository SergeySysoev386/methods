from itemadapter import ItemAdapter
from pymongo import MongoClient
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.social

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one({'user_id': item['user_id'], 'username': item['username'], 'account': item['account'],
                               'type': item['type'], 'photo': item['photo']})

        return item

class InstaparserPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            try:
                yield scrapy.Request(item['photo'])
            except Exception as x:
                print(x)
        return item

    def file_path(self, requests, response=None, info=None, *, item=None):
        return f"{item['account']}/{item['username']}.jpg"
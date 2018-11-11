# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class OfferscrawlersPipeline(object):
    def __init__(self):
    	db_url = 'mongodb://himp:95b8e3e76b9dd96e5f7c3b299864a655@dokku-mongo-himp:27017/himp'
        connection = pymongo.MongoClient(db_url)
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise  DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            pass
        return item    

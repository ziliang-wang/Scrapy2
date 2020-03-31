# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from guazi_project.handle_mongo import mongo


class GuaziProjectPipeline(object):
    def process_item(self, item, spider):
        item = dict(item)
        mongo.save_data('guazi_data', item)
        return item

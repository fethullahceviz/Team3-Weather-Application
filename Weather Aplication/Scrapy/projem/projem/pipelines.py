# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2

class ProjemPipeline(object):

    def open_spider(self, spider):
        self.connection = psycopg2.connect(host='localhost', user='postgres', password='123456', dbname='weather')
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        #self.cur.execute("INSERT INTO city_info(land,city,province,population) VALUES(%s,%s,%s,%s)",(item['land'],item['city'],item['province'],item['population']))
        #self.connection.commit()
        return item
        
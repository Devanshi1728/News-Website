# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
from datetime import datetime
from scrapy.pipelines.images import ImagesPipeline

class NewsPipeline(object):
    def _init_(self):
        pass

    def store_db(self, item):
        self.con = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'db_news'
        )
        self.curr = self.con.cursor(buffered=True)
        self.curr.execute("""SELECT id AS category_id FROM `app1_category`""")
        self.curr.execute("""SELECT id AS source_id FROM `app1_source`""")
        self.qry = "select count(*) from `app1_news` where headlines =\"%s\" " % (item['headlines'])
        self.curr.execute(self.qry)
        self.cnt = self.curr.fetchone()[0]
        print("ccccccccccc = ",self.cnt)
        print("COUNT ====",self.curr.rowcount)
        if self.cnt == 0:
            self.curr.execute("""INSERT INTO `app1_news`(headlines,  description, site, story, datetime, image_url, category_id, source_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",(
                item['headlines'],
                item['description'],
                item['site'],
                item['story'],
                item['datetime'],
                item['image_url'],
                item['category_id'],
                item['source_id']
            ))
            self.con.commit()
        else:
            pass
        self.con.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

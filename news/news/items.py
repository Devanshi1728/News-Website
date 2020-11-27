# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
      headlines = scrapy.Field()
      description = scrapy.Field()
      site = scrapy.Field()
      featured = scrapy.Field()
      story = scrapy.Field()
      datetime = scrapy.Field()
      image_url = scrapy.Field()
      category_id = scrapy.Field()
      source_id = scrapy.Field()
      
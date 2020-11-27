import scrapy
from ..items import NewsItem

class Spider1Spider(scrapy.Spider):
    name = 'spider_4'
    start_urls = ['https://www.indiatoday.in/india']

    def parse(self, response):
       items = NewsItem()
       #category_lst = ["india", "business", "world"]
       all_div = response.css('div.catagory-listing')
       for news in all_div:
           headlines = news.css("a::text").get()
           description = news.css("p::text").get()

           items['headlines'] = headlines
           items['description'] = description
           items['category_id'] = 1
           items['source_id'] = 1
           items['tag_id'] = 1

           yield items

    
            

    
            
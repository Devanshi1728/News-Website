import scrapy
import os
from ..items import NewsItem
from datetime import datetime

class Homepage3Spider(scrapy.Spider):
    name = 'Homepage3'
    allowed_domains = ['ndtv.com']
    start_urls = ['http://ndtv.com/']

    def parse(self, response):
        items = NewsItem() 
        current_url = response.url
        st = response.css("div.featured_cont ul li")
        for i in st:
            story = i.css("a::text").get() 
            site = i.css("a::attr(href)").get()
            img = i.css("a img::attr(src)").get()
            items['site'] = site
            items['story'] = story
            items['headlines'] = None
            items['description'] = None
            items['image_url'] = img
            items['datetime'] = datetime.now().strftime('%d %b %Y, %I:%M %p')
            items['source_id'] = 3
            items['category_id'] = 4
            yield items

            print("sTORY = ",story)
            print("site = ",site)

        all_div = response.xpath("/html/body/div[5]/div[2]/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]")   
        for news in all_div:
            headlines = news.xpath("h1/a/text()").get()  	#big Story
            image_url = news.xpath("a/img/@src").get()
            site = news.xpath("h1/a/@href").get() 	
        
            print("FEATURED = ",headlines)
            print("Site = ",site)
            print("Image url = ",image_url)

            items['site'] = site
            if headlines:
                items['headlines'] = headlines
            items['description'] = None
            items['image_url'] = image_url
            items['story'] = None
            items['datetime'] = datetime.now().strftime('%d %b %Y, %I:%M %p')
            items['source_id'] = 3
            items['category_id'] = 4
            
            yield items

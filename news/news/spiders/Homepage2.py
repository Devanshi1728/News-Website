import scrapy
from ..items import NewsItem
from datetime import datetime
from urllib.parse import urljoin

class Homepage2Spider(scrapy.Spider):
    name = 'Homepage2'
    allowed_domains = ['indianexpress.com']
    start_urls = ['http://indianexpress.com/']

    def parse(self, response):
        items = NewsItem() 
        current_url = response.url
        st = response.css("div.right-part div.top-news ul li")
        for i in st:
            story = i.css("h3 a::text").get() 
            site = i.css("h3 a::attr(href)").get()
            items['site'] = site
            items['story'] = story
            items['headlines'] = None
            items['description'] = None
            items['image_url'] = None
            items['datetime'] = datetime.now().strftime('%d %b %Y, %I:%M %p')
            items['source_id'] = 2
            items['category_id'] = 4
            yield items

            print("sTORY = ",story)
            print("site = ",site)

        all_div = response.css("div.left-part")   
        for news in all_div:
            headlines = news.css("div div.ie-first-story h2 a::text").get()  	#big Story
            image_url = news.css("div div.lead-img img::attr(src)").get()
            site = news.css("div div.ie-first-story h2 a::attr(href)").get() 	
        
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
            items['source_id'] = 2
            items['category_id'] = 4
            
            yield items


import scrapy
from ..items import NewsItem
from time import sleep
from datetime import datetime

class Spider2Spider(scrapy.Spider):
    name = 'spider2'
    start_urls = ['https://www.ndtv.com/']

    def parse(self, response):
        items = NewsItem()
        last_word = []
        category_lst = ["india", "world-news","business/latest"]
        if category_lst is not None:
            for i in category_lst:
                self.log(i)
                next_url = response.urljoin(i)
                print("Response url = ",response.url)
                yield scrapy.Request(next_url, callback=self.parse)

                all_div = response.css("div.new_storylising ul li")
               
                current_url = response.url
                last_word.append(current_url.split('/')[-1])
                print("Last------ word", last_word)
                print("Current url = ",current_url)
               
               #img_url = []
                for news in all_div:
                    headlines = news.css("h2.nstory_header a::attr(title)").get()
                    description = news.css("div.nstory_intro::text").get()
                    site = news.css("h2.nstory_header a::attr(href)").get()
                    img_url = news.css("img::attr(src)").get()
                    if headlines:
                        items['headlines'] = headlines.replace(":",",").replace('"',"")
                    items['description'] = description
                    items['site'] = site
                    items['story']=None
                    items['datetime'] = datetime.now().strftime('%d %b %Y, %I:%M %p')
                    items['image_url'] = img_url
                    
                    if "india" in last_word:
                        items['category_id'] = 1
                    elif "world-news" in last_word:
                        items['category_id'] = 2
                    elif "latest" in last_word:
                        items['category_id'] = 3
                    items['source_id'] = 3
                    yield items
                    
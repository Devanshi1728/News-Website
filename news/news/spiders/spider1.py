import scrapy
from ..items import NewsItem
from time import sleep
import schedule
import time
from datetime import datetime

class Spider1Spider(scrapy.Spider):
    name = 'spider1'
    start_urls = ['https://indianexpress.com/']

    def parse(self, response):
        items = NewsItem()
        last_word = []
        category_lst = ["section/india", "section/world", "section/business"]
        
        if category_lst is not None:
            for i in category_lst:
                self.log(i)
                next_url = response.urljoin(i)
                print("Response url = ",response.url)
                print("Next_url = ",next_url)
                if len(next_url.split("/")) < 7:
                    yield scrapy.Request(next_url, callback=self.parse)

                all_div = response.css("div.articles")
                current_url = response.url
                last_word.append(current_url.split("/")[-2])
                print("last - world",last_word)
                print("Current url = ",current_url)
                sleep(2)
                for news in all_div:
                    headlines = news.css("h2.title a::text").get() 
                    description = news.css("p::text").get()
                    image_url = news.css("div.snaps noscript img::attr(src)").get()
                    site = news.css("h2.title a::attr(href)").get()

                    if headlines:
                        items['headlines'] = headlines.replace(":",",").replace('"',"")
                    if description:
                        items['description'] = description
                    items['datetime'] = datetime.now().strftime('%d %b %Y, %I:%M %p')
                    items['site'] = site
                    items['story']=None
                    items['image_url'] = image_url
            
                    if "india" in last_word:
                        items['category_id'] = 1
                    elif "world" in last_word:
                        items['category_id'] = 2
                    elif "business" in last_word:
                        items['category_id'] = 3
                
                    items['source_id'] = 2
                   
                    yield items

if __name__ == '__main__':
    s1 = Spider1Spider()
    schedule.every(2).minutes.do(s1.parse)
    
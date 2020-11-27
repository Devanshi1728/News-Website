import scrapy
from ..items import NewsItem
from time import sleep
from urllib.parse import urljoin
from datetime import datetime

class Spider3Spider(scrapy.Spider):
    name = 'spider3'
    start_urls = ['https://www.indiatoday.in/']
    def parse(self, response):
        items = NewsItem()    
        last_word = []
        category_lst = ["india", "world", "business"]
        if category_lst is not None:
            for i in category_lst:
                self.log(i)
                next_url = response.urljoin(i)
                print("Response url = ",response.url)
                yield scrapy.Request(next_url, callback=self.parse)

                all_div = response.css('div.catagory-listing')
                current_url = response.url
                last_word.append(current_url.split('/')[-1])
                # print("LAST-WORD = ",last_word)
                # print("Current url = ",current_url)
                
                for news in all_div:
                    headlines = news.css("a::text").get()
                    description = news.css("p::text").get()
                    site = news.css("a::attr(href)").get()
                    image_url = news.css("img::attr(src)").get()
                    # print("CURL = ",current_url)
                    # print("RUrL = ",response.url)
                    # print("SIteeeeeeeee = ",urljoin(current_url,site))
                    if headlines:
                        items['headlines'] = headlines.replace('"',"").replace(":",",")
                    if description:
                        items['description'] = description
                    items['site'] = urljoin(current_url,site)
                    items['story']=None
                    items['datetime'] = datetime.now().strftime('%d %b %Y, %I:%M %p')
                    items['image_url'] = image_url
                    
                    if "india" in last_word:
                        items['category_id'] = 1
                    elif "world" in last_word:
                        items['category_id'] = 2
                    elif "business" in last_word:
                        items['category_id'] = 3
                                      
                    items['source_id'] = 1
                    yield items
        '''
        next_page=response.css("li.pager-item a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        '''
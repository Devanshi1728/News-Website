import scrapy
from twisted.internet import reactor
from multiprocessing import Process, Queue
from scrapy.crawler import CrawlerProcess
from items import NewsItem
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from datetime import datetime
import time
from urllib.parse import urljoin

class HomepageSpider(scrapy.Spider):
    name = 'Homepage'
    start_urls = ['https://www.indiatoday.in/']
    def parse(self, response):
        items = NewsItem() 
        current_url = response.url
        st = response.css("ul.itg-listing li")
        for i in st:
            story = i.css("a::attr(title)").get() 
            site = i.css("a::attr(href)").get()
            items['site'] = urljoin(current_url,site)
            items['story'] = story
            items['headlines'] = None
            items['description'] = None
            items['image_url'] = None
            items['datetime'] = datetime.now().strftime('%d %b %Y, %I:%M %p')
            items['source_id'] = 1
            items['category_id'] = 4
            yield items

            print("sTORY = ",story)
            print("site = ",site)

        all_div = response.css("div.featured-post")   
        for news in all_div:
            headlines = news.css("a::attr(title)").get()  	#big Story
            image_url = news.css("img::attr(src)").get()
            site = news.css("a::attr(href)").get() 	
        
            print("FEATURED = ",headlines)
            print("Site = ",site)
            print("Image url = ",image_url)

            items['site'] = site
            items['headlines'] = headlines
            items['description'] = None
            items['image_url'] = image_url
            items['story'] = None
            items['datetime'] = datetime.now().strftime('%d %b %Y, %I:%M %p')
            items['source_id'] = 1
            items['category_id'] = 4
            
            yield items

def sleep(_, duration=5):
    print(f'sleeping for: {duration}')
    time.sleep(duration)  # block here


def crawl(runner):
    d = runner.crawl(HomepageSpider)
    d.addBoth(sleep)
    d.addBoth(lambda _: crawl(runner))
    return d


def loop_crawl():
    runner = CrawlerRunner(get_project_settings())
    crawl(runner)
    reactor.run()


if __name__ == '__main__':
    loop_crawl()

import os
import json
import scrapy
from scrapy import Request
from ..items import SpiderItem

class StackOverflowSpider(scrapy.Spider):
    count = 0
    name = "bili"
    start_urls = [
        'https://www.bilibili.com/read/home'
    ]

    def start_requests(self):
        start_api = 'https://api.bilibili.com/x/article/recommends\?cid\=0\&pn\=1\&ps\=20\&jsonp\=jsonp\&aids\=\&sort\=0' 
        base_url = 'https://www.bilibili.com/read/cv'

        stream = os.popen("curl https://api.bilibili.com/x/article/recommends\?cid\=0\&pn\=1\&ps\=20\&jsonp\=jsonp\&aids\=\&sort\=0")
        jsonStr = stream.read()
        jsonObj = json.loads(jsonStr)
        pagesInfos = jsonObj['data']
        for pageInfo in pagesInfos:
            link = base_url + str(pageInfo['id'])
            yield scrapy.Request(url=link, callback=self.parse)

        
    def parse(self, response):
        self.count += 1
        items = SpiderItem()
        items['base_site'] = 'bilibili.com'

        # for q in response.css('.recommend-article-list>a'):
        #     items['title'] = q.css('span::text').get() 
        #     items['href'] = q.css('a::attr("href")').get()

        #     yield items
        
        for q in response.css('.article-item'):
            items['title'] = q.css('.article-title::text').get()
            items['href'] = q.css('a::attr("href")').get()

            yield items

        next_page = items.get('href')
        if next_page is not None and self.count < 10:
            yield response.follow(next_page, callback=self.parse)
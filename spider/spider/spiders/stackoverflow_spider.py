import scrapy
from ..items import SpiderItem


class StackOverflowSpider(scrapy.Spider):
    count = 0
    name = "stackoverflow"
    start_urls = [
        'https://stackoverflow.com/questions'
    ]
        
    def parse(self, response):
        self.count += 1
        items = SpiderItem()

        for q in response.css('.s-post-summary--content-title'):
            items['base_site'] = 'stackoverflow.com'
            items['title'] = q.css('a::text').get() 
            items['href'] = q.css('a::attr("href")').get()

            yield items
        
        next_page = response.css('.s-pagination--item.js-pagination-item[rel="next"]::attr("href")').get()
        if next_page is not None and self.count < 10:
            yield response.follow(next_page, callback=self.parse)
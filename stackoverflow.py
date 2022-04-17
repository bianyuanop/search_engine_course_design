import scrapy

class StackOverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    start_urls = [
        'https://stackoverflow.com/questions',
    ]

    def parse(self, response):
        for question in response.css('.s-post-summary--content>h3>a'):
            yield {
                'title' : question.css('a::text').get(),
                'href': question.css('a::attr("href")').get()
            }
        
        next_page = response.css('a.js-pagination-item::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
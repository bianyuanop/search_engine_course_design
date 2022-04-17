# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from fileinput import filename
import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    base_site = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    url = scrapy.Field()
    filename = scrapy.Field()
    words_file = scrapy.Field()

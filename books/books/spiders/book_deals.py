# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookDealsSpider(CrawlSpider):
    name = 'book_deals'
    allowed_domains = ['books.toscrape.com/']
    start_urls = ['https://books.toscrape.com/']

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="//ol[@class='row']"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield {
            'book_name': response.xpath("//li/article/h3/a/text()").get(),
            'price': response.xpath("//li/article/div[@class='product_price']/p[1]/text()").get(),
        }

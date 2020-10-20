# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookDealsSpider(CrawlSpider):
    name = 'book_deals'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com']

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://books.toscrape.com', headers={'User-Agent': self.user_agent})

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths="(//ol[@class='row']/li/article)"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//li[@class='next']/a)"),
             callback='parse_item', follow=True, process_request='set_user_agent')
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def make_num(self, num):
        return float(num.split("£")[1])

    def parse_item(self, response):
        yield {
            'book_name': response.xpath("//h3[1]/a[1]/text()").get(),
            'price': self.make_num(response.xpath("//div[@class='product_price']/p[1]/text()").get()),
            # 'user-agent': response.request.headers['User-Agent']
        }

# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top/']

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/', headers={'User-Agent': self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']//a"),
             callback='parse_item', follow=True, process_request='set_user_agent'),
    )
    # Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"),
    #      follow=True, process_request='set_user_agent')

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath("//div[@class='title_wrapper']/h1/text()").get(),
            'year': response.xpath("//div[@class='title_wrapper']/h1/span[@id='titleYear']/a/text()").get(),
            'duration': response.xpath("normalize-space(//div[@class='title_wrapper']/div[@class='subtext']/time/text())").get(),
            'genre': response.xpath("//div[@class='subtext']/a[1]/text()").get(),
            'rating': response.xpath("//div[@class='ratingValue']/strong/span/text()").get(),
            'movie_url': response.url,
            'user-agent': response.request.headers['User-Agent'],
        }


# "//td[@class='titleColumn']//a/@href"

# -*- coding: utf-8 -*-
import scrapy
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from news.items import NewsItem



class AdaderanaSpider(scrapy.Spider):
    name = 'adaderana'
    allowed_domains = ['www.adaderana.lk']
    start_urls = ['http://www.adaderana.lk/']


    
    def parse(self, response):
        print('Processing..' + response.url)
        title = response.css('title::text').extract()[0].strip()
        print("Title", title)
             
        latest = response.css('div.top-story h3 a::attr(href)').extract_first()
        url = response.urljoin(latest)
        yield scrapy.Request(url, callback=self.parse_latest)


        hotnews = response.css('div.hot-news.news-story a::attr(href)').extract()
        for a in hotnews:
             url = response.urljoin(a)
             yield scrapy.Request(url, callback=self.parse_headlines)

        
    def parse_latest(self, response):

        print(response.url)
        item = NewsItem()
        item['source'] = "AdaDerana"
        item['title'] = response.css('div.container.main-content h1::text').extract_first().strip()
        #print(item['title'])
        item['url'] = response.url
        item['time'] = response.css('div.container.main-content p.news-datestamp::text').extract_first().strip()

        body = response.css('div.news-content p').extract()

        btext = ''
        for e in body:
             btext += e.strip()
        item['body'] = btext
        if len(btext) > 10:
##             print(item)
             yield item
        


    def parse_headlines(self, response):

        print(response.url)
        item = NewsItem()
        item['source'] = "AdaDerana"
        item['title'] = response.css('div.container.main-content h1::text').extract_first().strip()
        #print(item['title'])
        item['url'] = response.url
        item['time'] = response.css('div.container.main-content p.news-datestamp::text').extract_first().strip()

        body = response.css('div.news-content p').extract()

        btext = ''
        for e in body:
             btext += e.strip()
        item['body'] = btext
        if len(btext) > 10:
##             print(item)
             yield item

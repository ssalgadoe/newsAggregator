# -*- coding: utf-8 -*-
import scrapy
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from news.items import NewsItem



class DailymirrorSpider(scrapy.Spider):
    name = 'dailymirror'
    allowed_domains = ['www.dailymirror.lk']
    start_urls = ['http://www.dailymirror.lk/']


    
    def parse(self, response):
        print('Processing..' + response.url)
        title = response.css('title::text').extract()[0].strip()
        print("Title", title)
        headline =  response.css('.col-md-4.col-sm-6 .panel-topst a::attr(href)').extract_first()
        latest = response.xpath("//div[@class='row']/div[@class='col-md-4 col-sm-6']/div[@class='row']/div[@class='panel panel-default panel-latestst']/div[@class='row']/a[@class='panel-heading']/@href").extract()
        
        yield scrapy.Request(headline, callback=self.parse_headline)
       
        for a in latest:
            yield scrapy.Request(a, callback=self.parse_latest)
##        yield item
        
    def parse_headline(self, response):
        item = NewsItem()
        item['source'] = "DailyMirror"
        item['title'] = response.css("h1.inner-hd::text").extract_first().strip()
        item['time'] = response.xpath("//div[@class='well well-lg']/text()").extract_first().strip()
        item['url'] = response.url
        body = response.css(".row.inner-text p::text").extract()
        btext = ''
        for e in body:
            if len(e.strip()) > 5 and '...' not in e.strip():
                btext += e.strip()
        item['body'] = btext
        yield item

        
    def parse_latest(self, response):
        print(response.url)
        item = NewsItem()
        item['source'] = "DailyMirror"
        item['title'] = response.css("h1.inner-hd::text").extract_first().strip()
        item['time'] = response.xpath("//div[@class='well well-lg']/text()").extract_first().strip()
        item['url'] = response.url
        body = response.css(".row.inner-text p::text").extract()
        btext = ''
        for e in body:
            if len(e.strip()) > 5 and '...' not in e.strip():
                btext += e.strip()
        item['body'] = btext
        yield item
        

# -*- coding: utf-8 -*-
import scrapy
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from news.items import NewsItem



class NewsfirstSpider(scrapy.Spider):
    name = 'newsfirst'
    allowed_domains = ['www.newsfirst.lk']
    start_urls = ['http://www.newsfirst.lk/']


    
    def parse(self, response):
        print('Processing..' + response.url)
        title = response.css('title::text').extract()[0].strip()
        print("Title", title)
             
        latest = response.css('div.col-md-12 a::attr(href)').extract()
        for a in latest:
             url = response.urljoin(a)
             #print(url)
             yield scrapy.Request(url, callback=self.parse_headlines)


        
        
    def parse_headlines(self, response):
##        print(response.url)
        item = NewsItem()
        item['source'] = "NewsFirst"
        item['title'] = response.css('h1.text-center::text').extract_first().strip()
        print(item['title'])

        item['url'] = response.url
        body = response.css("div.col-xs-12.thumb-para.more-read-para p").extract()
####        item['time'] = response.xpath("//div[@class='well well-lg']/text()").extract_first().strip()
##
        btext = ''
        for e in body:
             btext += e.strip()
        item['body'] = btext
        if len(btext) > 10:
             print(item)
             yield item
        

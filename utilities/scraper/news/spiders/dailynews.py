# -*- coding: utf-8 -*-
import scrapy
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from news.items import NewsItem



class DailynewsSpider(scrapy.Spider):
    name = 'dailynews'
    allowed_domains = ['www.dailynews.lk']
    start_urls = ['http://www.dailynews.lk/']


    
    def parse(self, response):
        print('Processing..' + response.url)
        title = response.css('title::text').extract()[0].strip()
        print("Title", title)
        headlines = response.xpath("//div[@class='views-field-title']/div[@class='views-content-title']/a/@href").extract()
##        print(headlines)
        for a in headlines:
             url = response.urljoin(a)
             yield scrapy.Request(url, callback=self.parse_headlines)
             
        latest = response.css('div.view.view-home-page.view-id-home_page.view-display-id-block_8 a::attr(href)' ).extract()
        for a in latest:
             url = response.urljoin(a)
             yield scrapy.Request(url, callback=self.parse_headlines)

        
        
    def parse_headlines(self, response):
        print(response.url)

        item = NewsItem()
        item['source'] = "DailyNews"
        item['title'] = response.xpath("//h1[@id='page-title']/text()").extract_first().strip()
        item['url'] = response.url
        body = response.xpath("//div[@class='field-items']/div[@class='field-item even']/p").extract()
##        item['time'] = response.xpath("//div[@class='well well-lg']/text()").extract_first().strip()

        btext = ''
        for e in body:
             btext += e.strip()
        item['body'] = btext
##        print(item)
        yield item
        

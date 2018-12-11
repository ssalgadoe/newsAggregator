import scrapy
from scrapy.crawler import CrawlerProcess
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




process = CrawlerProcess({
'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
'FEED_FORMAT': 'jl',
'FEED_URI': 'together_news.jl'
})
    
process.crawl(DailymirrorSpider)
process.crawl(AdaderanaSpider)
process.crawl(DailynewsSpider)
process.start()
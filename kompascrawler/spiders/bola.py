import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from kompascrawler import items
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class bola(CrawlSpider):
    name = 'bola'
    start_urls = ['http://bola.kompas.com/search']

    rules = (
    	Rule(LinkExtractor(allow=r'read/'),callback="parse_item"),
        Rule(LinkExtractor(restrict_xpaths='//a[@class="paging__link paging__link--next"]'))
    	)
    def parse_item(self, response):
    	item = items.KompascrawlerItem()
    	item['title'] = response.xpath('//h1[@class="read__title"]/text()').extract()
    	str_cont = response.xpath('//div[@class="read__content"]/p//text()').extract()
        print str_cont
        if "kompas.com" in str_cont[0].lower():
            str_cont = " ".join(str_cont[1:])
        else:
            str_cont = " ".join(str_cont)
        str_cont = str_cont.encode('UTF-8')
        str_cont = re.sub(r'[^\x00-\x7f]',r' ',str_cont)
        str_cont = str_cont.decode()
        str_cont = str_cont.replace("\n"," ")
        str_cont = str_cont.strip()
        if str_cont[0] == "-":
            str_cont = str_cont[1:]
        str_cont = re.sub('\s+',' ',str_cont).strip()
    	item['content'] = str_cont

    	return item
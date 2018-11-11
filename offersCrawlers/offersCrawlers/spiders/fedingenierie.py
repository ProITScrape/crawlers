# -*- coding: utf-8 -*-
import scrapy
import logging
from offersCrawlers.items import OfferscrawlersItem
from urlparse import urlparse


import re
class FedingenierieSpider(scrapy.Spider):
    name = 'fedingenierie'
    start_urls = ['http://www.fedingenierie.fr/nos-offres-demploi-ingenieurs-et-techniciens/']

    def __init__(self, category=None, *args, **kwargs):
        self.search_url='http://www.fedingenierie.fr/nos-offres-demploi-ingenieurs-et-techniciens/'
        parsed_uri = urlparse(self.search_url)
        self.domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
     
    def parse(self, response):
    	offers=response.xpath('//ul[@class="liste-content"]/li')
    	for offer in offers:
    		offer_link=response.urljoin(offer.xpath('./a/@href').extract_first())
    		yield scrapy.FormRequest(offer_link,callback=self.extract_data)
		next_page_link=response.urljoin(response.xpath('//li[@class="pager-next"]/a/@href').extract_first())
		yield scrapy.FormRequest(next_page_link,callback=self.parse)

    def extract_data(self, response):
    	item=OfferscrawlersItem()
    	description=[]
    	item['date']=response.xpath('//span[@itemprop="datePosted"]/text()').extract_first()
        item['title']=response.xpath('//h2[@itemprop="title"]/text()').extract_first()
        item['location']=response.xpath('//span[@itemprop="jobLocation"]/text()').extract_first()
        item['company']=response.xpath('//meta[@property="og:site_name"]/@content').extract_first()
        ##### get description
        first_part=response.xpath('//div[@class="content-annonce"]/h3[1]/text()').extract_first()
        description.append(first_part)
        second_part=response.xpath('//div[@class="content-annonce"]/p[2]//text()').extract()
        for row in second_part:
        	description.append(row)
        third_part=response.xpath('//div[@class="content-annonce"]/h3[2]/text()').extract_first()
        description.append(third_part)
        fourth_part=response.xpath('//div[@class="content-annonce"]/p[3]//text()').extract()
        for row in fourth_part:
        	description.append(row)
        five_part=response.xpath('//div[@class="content-annonce"]/h3[3]/text()').extract_first()
        description.append(five_part)
        sixth_part=response.xpath('//div[@class="content-annonce"]/p[4]//text()').extract()
        for row in sixth_part:
        	description.append(row)

        ##### end description 
        item['description']=description
        
        item['url']=response.url
        item['offerId']=""
        item['provider']=self.domain
        item['status']="current"
        item['contractKind']=response.xpath('//span[@itemprop="employmentType"]/text()').extract_first()
        item['sector']=response.xpath('//ul[@class="breadcrumb"]/li[3]/a/text()').extract_first()
    	item['companyId']=""
        item['remuneration']=response.xpath('//span[@itemprop="incentives"]/text()').extract_first()
        item['reference']=re.search(r"Référence de l'offre :(.*?)<", response.body).group(1).strip()

    	yield item 



    	self.crawler.stats.get_stats()
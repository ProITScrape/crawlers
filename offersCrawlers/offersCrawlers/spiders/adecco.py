# -*- coding: utf-8 -*-
import scrapy
import logging
from offersCrawlers.items import OfferscrawlersItem
from urlparse import urlparse
from scrapy import signals
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest

class AdeccoSpider(scrapy.Spider):
    name = 'adecco'
    allowed_domains = ['adecco.fr']
    start_urls=['https://www.adecco.fr/resultats-offres-emploi/?k=&l=&display=15&buname=adecco.fr%7cadeccomedical.fr%7cadeccopme.fr']
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
      spider = super(AdeccoSpider, cls).from_crawler(crawler, *args, **kwargs)
      crawler.signals.connect(spider.spider_closed, signals.spider_closed)
      return spider

    def __init__(self, task, *args, **kwargs):
    	self.task=task
    	parsed_uri = urlparse(self.start_urls[0])
        self.domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
	


    
    def parse(self, response):
        get_list_offers_links=response.xpath('//a[@class="btn btn-sm btn-success pull-right"]/@href').extract()
        for link in get_list_offers_links:
        	yield scrapy.FormRequest(link,callback=self.extract_offer_data,dont_filter=True)
        next_page_link=response.urljoin(response.xpath('//a[@id="paginationSuivant"]/@href').extract_first())
        yield scrapy.FormRequest(next_page_link,callback=self.parse)
    def extract_offer_data(self,response):
        item=OfferscrawlersItem()
        localisation=""
        date_posted=response.xpath('//span[@id="posted-date"]/text()').extract_first()
        title=response.xpath('normalize-space(//h1/text())').extract_first()
        city=response.xpath('//span[@id="lblCity"]/text()').extract_first()
        state=response.xpath('//span[@id="lblState"]/text()').extract_first()
        if city != None and state != None:
           localisation=city+state
        else:
            if city != None:
                localisation=city
            if state != None:
                localisation=state

        contract_type=response.xpath('//span[@id="ltEmploymentType"]/text()').extract_first()
        emploi_type=response.xpath('normalize-space(//span[@id="ltContractType"]/text())').extract_first()
        company=response.xpath('//div[@id="branchName"]//text()').extract_first()
        description=response.xpath('//div[@class="job--task-specifics"]//text()').extract()
        remuneration=response.xpath('//span[@id="ltSalaryWage"]/text()').extract_first()
        reference=response.xpath('normalize-space(//p[@class="reference-number"]/span/text())').extract_first()
        
        item['date']=date_posted
        item['title']=title
        item['location']=localisation
        item['contractKind']=contract_type
        item['company']=company
        item['companyId']=""
        item['description']=description
        item['remuneration']=remuneration
        item['url']=response.url
        item['offerId']=""
        item['reference']=reference
        item['provider']=self.domain
        item['status']="current"
        item['sector']=response.xpath('normalize-space(//span[@id="ltIndustry"]/text())').extract_first()
        yield item

    def spider_closed(self, spider):
        base_url=settings['BASE_URL']
        print base_url
        base_url=base_url+"/tasks/"+self.taskId
        headers = {'Content-type':'application/json'}
        data=self.crawler.stats.get_stats()
        log_count_ERROR=0
        item_scraped_count=0
        if 'log_count/ERROR' in data.keys():
            log_count_ERROR=data['log_count/ERROR']
        if 'item_scraped_count'    in data.keys():
            item_scraped_count=data['item_scraped_count']

        formdata={
            "taskId": self.taskId,
              "crawlerType":"adecco",
              "stats":self.crawler.stats.get_stats(),
              "log_count/ERROR":log_count_ERROR,
              "duration":data['finish_time']-data['start_time'],
              "numberOffersCrawled":item_scraped_count
        }
        yield FormRequest(base_url,method="PUT", formdata=frmdata,headers=headers)

    	
    	
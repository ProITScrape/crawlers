# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OfferscrawlersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date=scrapy.Field()
    title=scrapy.Field()
    location=scrapy.Field()
    contractKind=scrapy.Field()
    company=scrapy.Field()
    companyId=scrapy.Field()
    description=scrapy.Field()
    remuneration=scrapy.Field()
    url=scrapy.Field()
    reference=scrapy.Field()
    offerId=scrapy.Field()
    status=scrapy.Field()
    provider=scrapy.Field()
    sector=scrapy.Field()
    

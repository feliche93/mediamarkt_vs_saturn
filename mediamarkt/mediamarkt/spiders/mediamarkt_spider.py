# -*- coding: utf-8 -*-
import scrapy


class MediamarktSpiderSpider(scrapy.Spider):
    name = 'mediamarkt_spider'
    allowed_domains = ['mediamarkt.de']
    start_urls = ['http://mediamarkt.de/']

    def parse(self, response):
        categories = response.xpath(
            '//div[@class="mms-srp-tree__content mms-srp-tree__content--expanded"]')
        if len(categories) >= 2:
            categories = categories[0]
            category_urls = categories.xpath('.//a/@href').extract()
            category_texts = categories.xpath('.//a/text()').extract()
            for category_url, category_text in zip(category_urls, category_texts):
                print(category_url, category_text)
                scrapy.Request(url=category_url, callback=parse_category_one)

    def parse_category_one(self):
        pass

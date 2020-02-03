# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import re


class MediamarktSpider(scrapy.Spider):
    name = 'mediamarkt_spider'
    allowed_domains = ['mediamarkt.de']
    df = pd.read_csv(
        '/Users/felixvemmer/Desktop/mediamarkt_vs_saturn/start_urls.csv')
    start_urls = df['start_urls'].to_list()
    start_urls = start_urls[0:2]
    #start_urls = ['http://mediamarkt.de/']

    def parse(self, response):
        categories = response.xpath(
            '//div[@class="mms-srp-tree__content mms-srp-tree__content--expanded"]')
        if len(categories) >= 1:
            categories = categories[0]
            category_urls = categories.xpath('.//a/@href').extract()
            category_texts = categories.xpath('.//a/text()').extract()
            for category_url, category_text in zip(category_urls, category_texts):
                print(category_url, category_text)

                yield scrapy.Request(url=category_url, callback=self.parse_next_category, meta={
                    'category_one_url': category_url, 'category_one_text': category_text})

    def parse_next_category(self, response):
        categories = response.xpath(
            '//li[@class="mms-srp-tree-facet__item mms-srp-tree-facet__item--level-2"]')
        if categories:
            category_urls = categories.xpath('.//a/@href').extract()
            category_texts = categories.xpath('.//a/text()').extract()

            for category_url, category_text in zip(category_urls, category_texts):
                print(category_url, category_text)
                yield scrapy.Request(url=category_url, callback=self.parse_product_links, meta={
                    'category_one_url': response.meta['category_one_url'],
                    'category_one_text': response.meta['category_one_text'],
                    'category_two_url': category_url,
                    'category_two_text': category_text})

    def parse_product_links(self, response):

        product_urls = response.xpath(
            '//a[@class="mms-link mms-srp-product mms-link--default"]/@href').extract()

        for product_url in product_urls:
            product_url = 'https://mediamarkt.de' + product_url

            yield scrapy.Request(url=product_url, callback=self.parse_product_details, meta={
                'category_one_url': response.meta['category_one_url'],
                'category_one_text': response.meta['category_one_text'],
                'category_two_url': response.meta['category_two_url'],
                'category_two_text': response.meta['category_two_text']
            })

    def parse_product_details(self, response):

        product_name = response.xpath('//h1/text()').extract_first()

        # Check if can be fixed later
        normal_price = response.xpath(
            '//div[@class="mms-price mms-price--normal mms-price--strike"]')
        if normal_price:
            normal_price = normal_price.xpath(
                './/span[@class="mms-price__price"]//text()').extract()
            normal_price = ''.join(normal_price)

            try:
                normal_price = re.search(
                    r"[1-9]*[.][1-9]*", normal_price).group()
            except:
                print(normal_price)
                normal_price = None

        discounted_price = response.xpath(
            '//div[@class="mms-price mms-price--normal"]')
        if discounted_price:
            discounted_price = discounted_price.xpath(
                './/span[@class="mms-price__price"]//text()').extract()
            discounted_price = ''.join(discounted_price)
            try:

                discounted_price = re.search(
                    r"[1-9]*[.][1-9]*", discounted_price).group()

            except:
                print(discounted_price)
                discounted_price = None

        rating = response.xpath(
            '//span[@itemprop="ratingValue"]/text()').extract_first()

        paragraphs = response.xpath('//p//text()').extract()

        number_of_ratings = None
        article_number = None

        for paragraph in paragraphs:
            if 'Basierend' in paragraph:
                number_of_ratings = paragraph
                number_of_ratings = re.search(
                    r"\d", number_of_ratings).group()

            if 'Artikelnummer' in paragraph:
                article_number = paragraph
                article_number = article_number.split(': ')[1]

        yield {
            'category_one_url': response.meta['category_one_url'],
            'category_one_text': response.meta['category_one_text'],
            'category_two_url': response.meta['category_two_url'],
            'category_two_text': response.meta['category_two_text'],
            'product_name': product_name,
            'normal_price': normal_price,
            'discounted_price': discounted_price,
            'article_number': article_number,
            'rating': rating,
            'number_of_ratings': number_of_ratings
        }


process = CrawlerProcess(settings={
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'test_crawl.csv',
    # 'USER_AGENT' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
})

process.crawl(MediamarktSpider)
process.start()

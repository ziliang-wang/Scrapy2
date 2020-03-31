# -*- coding: utf-8 -*-
import scrapy
from guazi_project.handle_mongo import mongo

import re
from guazi_project.items import GuaziProjectItem


class GuaziSpider(scrapy.Spider):
    name = 'guazi'
    allowed_domains = ['www.guazi.com']
    # start_urls = ['http://guazi.com/']
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.guazi.com",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }

    def start_requests(self):
        while True:
            task = mongo.get_task('guazi_task')
            if not task:
                break
            if '_id' in task:
                task.pop('_id')
            print('task: ', task)
            yield scrapy.Request(url=task['task_url'],
                                 callback=self.parse,
                                 dont_filter=True,
                                 headers=self.header,
                                 meta=task)

    def parse(self, response):
        if '为您找到0辆好车' in response.text:
            print('无无无无无无')
            return
        list_items = response.xpath('//ul[@class="carlist clearfix js-top"]/li')
        for item in list_items:
            car_dict = {}
            car_dict['car_location'] = response.request.meta['city_name']
            car_dict['car_brand'] = response.request.meta['brand_name']
            car_dict['car_name'] = item.xpath('./a/@title').extract_first()
            car_dict['car_url'] = 'https://guazi.com' + item.xpath('./a/@href').extract_first()

            # print(car_dict['car_name'], car_dict['car_url'])
            yield scrapy.Request(url=car_dict['car_url'],
                                 callback=self.parse_details,
                                 meta=car_dict,
                                 dont_filter=True,
                                 headers=self.header)
        # print(f'共{counter}笔')
        # print('/'.join(response.request.meta['task_url'].split('/')[:-1]) + f'/o{555}i7')

        if response.xpath('//a[@class="next"]/span/text()').extract_first() == '下一页':
            current_page = int(response.xpath('//li[@class="link-on"]/a/span/text()').extract_first())
            # next_url_search = re.compile(r'https://www.guazi.com/(.*?)/(.*?)/o(\d+)i7')
            next_url = '/'.join(response.url.split('/')[:-1]) + f'/o{current_page+1}i7'
            response.request.meta['task_url'] = next_url

            yield scrapy.Request(url=response.request.meta['task_url'],
                                 callback=self.parse,
                                 headers=self.header,
                                 meta=response.request.meta,
                                 dont_filter=True)

    def parse_details(self, response):
        guazi_item = GuaziProjectItem()
        # car_id_search = re.compile(r'车源号：(.*?)\s+')
        # guazi_item['car_id'] = car_id_search.search(response.text).group(1)

        guazi_item['car_id'] = response.xpath('//div[@class="right-carnumber"]/text()'
                                              ).extract_first()[4:].strip()
        guazi_item['car_location'] = response.request.meta['car_location']
        guazi_item['car_brand'] = response.request.meta['car_brand']
        guazi_item['car_name'] = response.request.meta['car_name']
        guazi_item['car_url'] = response.request.meta['car_url']
        guazi_item['car_price'] = response.xpath('//span[@class="price-num"]/text()').extract_first()
        guazi_item['car_jr_price'] = response.xpath('//span[@class="price-jr-num"]/text()').extract_first()
        guazi_item['license_time'] = response.xpath('//li[@class="one"]/span/text()').extract_first()
        guazi_item['car_meter'] = response.xpath('//li[@class="two"]/span/text()').extract_first()
        guazi_item['displacement'] = response.xpath('//li[@class="three"]/span/text()').extract_first()
        guazi_item['transmission_case'] = response.xpath('//li[@class="last"]/span/text()').extract_first()
        yield guazi_item




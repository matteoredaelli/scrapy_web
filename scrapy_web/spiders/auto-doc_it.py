# -*- coding: utf-8 -*-

#   scrapy_web
#    Copyright (C) 2016-2017 Matteo.Redaelli@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# usage:
#   scrapy crawl lafeltrinelli -t jsonlines -o data/a.json

import scrapy
import datetime, re

class AutoDocIt(scrapy.Spider):
    name = "auto-doc.it"
    
    def __init__(self, width="195", height="65", diameter="15", *args, **kwargs):
        super(AutoDocIt, self).__init__(*args, **kwargs)
        self.allowed_domains = ["auto-doc.it"]
        # self.start_urls = ['http://www.auto-doc.it/pneumatici?Width=%s&CrossSections=%s&Size=%s&Season=&page=1' % (width, height, diameter)]
        self.start_urls = ['http://www.auto-doc.it/pneumatici/%d-pollici?page=1' % n for n in [10,12,13,14,15,16,17,18,19,20,21,22,23,24,40,365,390,415]]
    def parse(self, response):
        ts = datetime.datetime.now()
        for entry in response.xpath('//li[@class="ovVisLi"]'):
            id = entry.xpath('.//div[@class="description"]//span[@style="font-size: 12px;"]/text()').extract_first()
            ean = entry.xpath('.//span[@class="article_number"]/text()').extract_first()
            model = entry.xpath('.//div[@class="name"]/a/text()').extract_first()
            description = entry.xpath('.//div[@class="nr"]/text()').extract_first()
            price = entry.xpath('.//p[@class="actual_price"]/text()').extract_first()
            picture_url = entry.xpath('.//img[@class="tires_item_image "]/@src').extract_first()
            product_url = entry.xpath('.//div[@class="image"]/a/@href').extract_first()
            details =  {
                #"brand": brand,
                "description": description,
                "ean": ean,
                "id": id,
                "price": price,
                "model": model,
                #"season": season,
                #"size": size,
                "source": "auto-doc.it",
                "picture_url": picture_url,
                "product_url": product_url,
                "ts": ts
            }
            keys = entry.xpath('.//div[@class="description"]//div[@class="box"]//ul/li/span[@class="lc"]/text()').extract()
            ## removing : at the end
            keys = map(lambda x: x.replace(":",""), keys)
            values = entry.xpath('.//div[@class="description"]//div[@class="box"]//ul/li/span[@class="rc"]/text()').extract()
            details2 = zip(keys, values)
            details.update(details2)
            yield details
            
        next_page = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_page != None:
            yield scrapy.Request(next_page, callback=self.parse)
            
            




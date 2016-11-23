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
import re

class Lafeltrinelli(scrapy.Spider):
    name = "lafeltrinelli"
    allowed_domains = ["lafeltrinelli.it"]
    start_urls = ['http://www.lafeltrinelli.it/libri/c-1/0/%d/?cat1=1&pub=7&type=1&sort=3&pageSize=40' % n for n in range(1, 126)]

    def parse(self, response):
        for entry in response.xpath('//div[@class="product-result clearfix product-slider-2015"]/div'):
            id = entry.xpath('@id').extract_first()
            title = entry.xpath('div[@class="cover"]//@alt').extract_first()
            description_url = entry.xpath('div[@class="cover"]//@href').extract_first()
            cover_image_url = entry.xpath('div[@class="cover"]//img/@src').extract_first()
            author = entry.xpath('//h4/a//text()').extract_first()
            price = entry.xpath('//div[@class="add-to-cart"]//strong/text()').extract_first()
            yield {
                "author": author,
                "cover_image_url": cover_image_url,
                "description_ulr": description_url,
                "id": id,
                "price": price,
                "source": "lafeltrinelli.it",
                "title": title,
            }



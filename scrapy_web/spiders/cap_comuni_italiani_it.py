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
#   scrapy crawl cap-comuni-italiani -t jsonlines -o data/comuni-italiani.it/cap-comuni-italiani.json

import scrapy
import re

class CapComuniItalianiSpider(scrapy.Spider):
    name = "cap-comuni-italiani"
    allowed_domains = ["comuni-italiani.it"]
    start_urls = (
        'http://www.comuni-italiani.it/alfa/001.html',
    )

    def parse(self, response):
        for url in response.xpath('//table[@border="1"]//a/@href').extract():
            if bool(re.search("^\d\d\d\.html", url)):
                absolute_url = response.urljoin(url)
                yield scrapy.Request(absolute_url, callback=self.parse)
            elif bool(re.search("index.html", url)):
                absolute_url = response.urljoin(url)
                yield scrapy.Request(absolute_url, callback=self.parse_city)
    
    def parse_city(self, response):
        record = {}
        record['comune'] = response.xpath('//h1/text()').extract_first().replace("Comune di ","")
        for row in response.xpath('//tr'):
            if row.xpath('td[@class="ivoce"]'):
                field = row.xpath('td[@class="ivoce"]//text()').extract_first()
                value = row.xpath('td[2]//text()').extract_first()
                record[field] = value
        yield record


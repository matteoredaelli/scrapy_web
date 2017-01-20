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



# scrapy  crawl sapere.it -t jsonlines -o sapere.it.json

import scrapy

class SapereItSpider(scrapy.Spider):
    name = "aranzulla.it"
    allowed_domains = ["aranzulla.it"]
    start_urls = (
        'http://www.aranzulla.it/computer',
        'http://www.aranzulla.it/internet',
        'http://www.aranzulla.it/telefonia',
    )

    def parse(self, response):
        for url in response.xpath('//ul[@class="children"]//li/a/@href').extract():
            yield scrapy.Request(url, callback=self.parse_questions)
    
    def parse_questions(self, response):
        for entry in response.xpath('//li[@class="separator"]/a'):
            q = entry.xpath('./span/text()').extract_first()
            a = entry.xpath('./@href').extract_first()
            yield {"question": q,
                   "answer":  a,
                   "source": "aranzulla.it"}

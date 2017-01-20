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
    name = "sapere.it"
    allowed_domains = ["sapere.it"]
    start_urls = (
        'http://www.sapere.it/sapere/strumenti/domande-risposte.html',
    )

    def parse(self, response):
        for url in response.xpath('//h2/a/@href').extract():
            url = response.urljoin(url) + "?page=1"
            yield scrapy.Request(url, callback=self.parse_questions)
    
    def parse_questions(self, response):
        for entry in response.xpath('//h4/a'):
            q = entry.xpath('./text()').extract_first()
            a = entry.xpath('./@href').extract_first()
            yield {"question": q,
                   "answer":  "http://www.sapere.it" + a,
                   "source": "sapere.it"}
                    
        ### extracting next pages
        next_page = response.xpath('//li[@class="page-current-false page-active-true page-next"]/a/@href').extract_first()
        if next_page is not None and next_page != "#":
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_questions)

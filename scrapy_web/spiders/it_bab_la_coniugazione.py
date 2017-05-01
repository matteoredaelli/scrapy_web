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

# scrapy  crawl  -t jsonlines -o verbi.json it.bab.la

import scrapy

class itBabLaSpider(scrapy.Spider):
    name = "it.bab.la"
    allowed_domains = ["it.bab.la"]
    start_urls = ['http://it.bab.la/coniugazione/italiano/%s/' % n for n in map(chr, range(ord('A'), ord('Z')+1))]
  
    def parse(self, response):
        for next_page in response.xpath('//div[@class="toc-links"]//a/@href').extract():
            if next_page is not None and next_page != "#":
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_verbs)

    def parse_verbs(self, response):
        for next_page in response.xpath('//nav[@class="dict-select-wrapper"]//a/@href').extract():
            if next_page is not None and next_page != "#":
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_verb)
                
    def parse_verb(self, response):
        verbo = response.xpath('//strong/text()').extract_first()
        for tempoxml in response.xpath('//div[@class="conj-tense-block"]'):
            tempo = tempoxml.xpath('./h3/text()').extract_first()
            persone = tempoxml.xpath('.//div[@class="conj-item"]/div[@class="conj-person"]/text()').extract()
            coniugazione = tempoxml.xpath('.//div[@class="conj-item"]/div[@class="conj-result"]/text()').extract()
            yield {"verbo": verbo,
                       "tempo": tempo,
                       "persone": persone,
                       "coniugazione": coniugazione}

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



# scrapy  crawl dizionario_italiano_corriere -t jsonlines -o diz.json

import scrapy

class AcronimiComSpider(scrapy.Spider):
    name = "acronimi.com"
    allowed_domains = ["acronimi.com"]
    start_urls = (
        'http://acronimi.com/general_index',
    )

    def parse(self, response):
        #for url in response.xpath('//div[@id="ris-main"]/ul/li/a/@href').extract():
        #    if url is not None:
        #        absolute_url = response.urljoin(url)
        #        yield scrapy.Request(absolute_url, callback=self.parse_word)
        for url in response.xpath('//ul[@id="general-index"]//li/a/@href').extract():
            yield scrapy.Request(url, callback=self.parse_word)
            
            # extracting next pages
            next_page = response.xpath('//li[@class="next"]//a/@href').extract_first()
            if next_page is not None and next_page != "#":
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
    
    def parse_word(self, response):
        word = response.xpath('//title/text()').extract_first().split(' ')[0]
        yield {"word": word,
                   "meanings":  response.xpath('//ol/li/text()').extract(),
                   "source": "acronimi.com"}

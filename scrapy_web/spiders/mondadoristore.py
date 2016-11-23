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

class MondadoriStore(scrapy.Spider):
    name = "mondadoristore"
    allowed_domains = ["mondadoristore.it"]
    start_urls = ['http://www.mondadoristore.it/Libri-novita-e-ultime-uscite/gr-3920/']

    def parse(self, response):
        for entry in response.xpath('//div[@class="single-box product no-border"]'):
            id = entry.xpath('./a/@eancode').extract_first()
            title = entry.xpath('.//h3/a/@title').extract_first()
            description_url = entry.xpath('.//h3/a/@href').extract_first()
            cover_image_url = entry.xpath('.//a[@class="link"]/img/@src').extract_first()
            author = entry.xpath('.//a[@class="link nti-author"]/text()').extract_first()
            author_url = entry.xpath('.//a[@class="link nti-author"]/@href').extract_first()
            price = entry.xpath('.//span[@class="new-price"]/text()').extract_first()
            yield {
                "author": author,
                "cover_image_url": response.urljoin(cover_image_url),
                "description_ulr": description_url,
                "id": id,
                "price": price,
                "source": "mondadoristore.it",
                "title": title,
            }
            # extracting next pages
            for next_page in response.xpath('//a[@rel="next"]/@href').extract():
                if next_page is not None and next_page != "#":
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)



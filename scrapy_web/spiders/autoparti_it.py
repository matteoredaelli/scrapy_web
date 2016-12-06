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

import scrapy
import datetime, re

def clean_text(text):
    if text is None or text == "":
        return text

    t = re.sub('[\n\t\r]', '', text)
    return re.sub('  +', ' ', t).strip()
    
class AutopartiIt(scrapy.Spider):
    name = "autoparti.it"
    allowed_domains = ["autoparti.it"]
    start_urls = ['http://www.autoparti.it/pneumatici/%d-pollici?page=1' % n for n in [14,15,16,17,18]]

    def parse(self, response):
        ts = datetime.datetime.now()
        for entry in response.xpath('//div[@class="tires_listing"]/div[@class="item"]'):
            model = entry.xpath('//a[@class="prod_link"]/text()').extract_first()
            description = entry.xpath('.//span[@class="nam_model"]/text()').extract_first()
            ean = entry.xpath('.//div[@class="nr"]/span[1]/text()').extract_first()#.replace("EAN: ","")
            id  = entry.xpath('.//div[@class="nr"]/span[2]/text()').extract_first()#.replace("MPN: ","")
            picture_url = entry.xpath('.//img[@class="tires_item_image"]/@src').extract_first()
            prod_url = entry.xpath('.//a[@class="prod_link"]/@href').extract_first()
            price = entry.xpath('.//span[@class="new_pr"]/text()').extract_first()
            season = entry.xpath('.//div[contains(@class, "tires_season")]/@class').extract_first()#.replace("tires_season ","")
            yield {"id": id,
                       "description": description,
                       "ean": ean,
                       "model": model,
                       "picture_url": picture_url,
                       "prod_url": prod_url,
                       "price": price,
                       "season": season,
                       "source": "autoparti.it",
                       "ts": ts}

        next_page = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_page != None:
            yield scrapy.Request(next_page, callback=self.parse)
            
            




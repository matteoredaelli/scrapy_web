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

class NomiMaschiliFemminiliNomixItSpider(scrapy.Spider):
    name = "nomi-nomix.it"
    allowed_domains = ["nomix.it"]
    start_urls = (
        'http://www.nomix.it/nomi-italiani-maschili-e-femminili.php',
    )

    def parse(self, response):
        for nome in response.xpath('//div[@class="pure-g"]/div[1]/table//td/text()').extract():
            yield {"word": nome,
                   "class": "nome proprio",
                   "sex": "male",
                   "source": "nomix.com"}
        for nome in response.xpath('//div[@class="pure-g"]/div[2]/table//td/text()').extract():
            yield {"word": nome,
                   "class": "nome proprio",
                   "sex": "female",
                   "source": "nomix.com"}
            
        # extracting next pages
        for next_page in response.xpath('//h2/a/@href').extract():
            if next_page is not None and next_page != "#":
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)
    

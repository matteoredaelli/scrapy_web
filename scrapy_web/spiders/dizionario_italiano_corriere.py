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

class DizionarioItalianoCorriereSpider(scrapy.Spider):
    name = "dizionario_italiano_corriere"
    allowed_domains = ["dizionari.corriere.it"]
    start_urls = (
        'http://dizionari.corriere.it/dizionario_italiano/a.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/b.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/c.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/d.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/e.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/f.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/g.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/h.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/i.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/j.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/k.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/l.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/m.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/n.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/o.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/p.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/q.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/r.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/s.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/t.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/u.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/v.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/w.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/x.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/y.shtml',
        'http://dizionari.corriere.it/dizionario_italiano/z.shtml',
    )

    def parse(self, response):
        #for url in response.xpath('//div[@id="ris-main"]/ul/li/a/@href').extract():
        #    if url is not None:
        #        absolute_url = response.urljoin(url)
        #        yield scrapy.Request(absolute_url, callback=self.parse_word)
        for row in response.xpath('//div[@id="ris-main"]/ul/li'):
            word = row.xpath('a/strong/text()').extract_first()
            gramma = row.xpath('text()').extract_first()
            yield { "word": word, "gramma": gramma}
            
            # extracting next pages
            for next_page in response.xpath('//div[@id="ris-nav"]//a/@href').extract():
                if next_page is not None and next_page != "#":
                    next_page = response.urljoin(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)
    
    def parse_word(self, response):
        yield {"word": response.xpath('//div[@id="defin-dx"]/h1/text()').extract_first(),
                   "sillabazione": response.xpath('//div[@id="defin-dx"]//h5/strong[1]/text()').extract_first(),
                   "grammatica": response.xpath('//div[@id="defin-dx"]//h5/strong[2]/text()').extract_first()}



# extract first definition
# from w3lib.html import remove_tags
# text=response.xpath('//div[@id="defin-dx"]/ul/li[1]/p').extract_first()
# remove_tags(text)

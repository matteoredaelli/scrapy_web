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
import datetime, re

class GommadirettoIt(scrapy.Spider):
    name = "gommadiretto.it"
    
    def __init__(self, width="195", height="65", diameter="15", *args, **kwargs):
        super(GommadirettoIt, self).__init__(*args, **kwargs)
        self.allowed_domains = ["gommadiretto.it"]
        self.start_urls = ['http://www.gommadiretto.it/cgi-bin/rshop.pl?s_p=&rsmFahrzeugart=PKW&s_p_=Tutti&dsco=130&tyre_for=&search_tool=&ist_hybris_orig=&with_bootstrap_flag=1&suchen=--Mostrare+tutti+gli+pneumatici--&m_s=3&x_tyre_for=&cart_id=88618236.130.22966&sowigan=&Breite=%s&Quer=%s&Felge=%s&Speed=&Load=&Marke=&kategorie=&filter_preis_von=&filter_preis_bis=&homologation=&Ang_pro_Seite=50' % (width, height, diameter) ]
        
    def parse(self, response):
        ts = datetime.datetime.now()
        for entry in response.xpath('//div[@class="artikelklotz ajax_artikelklotz ajax_suchergebnisliste_artikelklotz"]'):
            id = entry.xpath('.//a/@name').extract_first()
            brand = entry.xpath('.//div[@class="formcaddyfab"]//font/text()').extract_first()
            price1 = entry.xpath('.//div[@class="price"]//b/text()').extract_first()
            price2 = entry.xpath('.//div[@class="price"]//small/text()').extract_first()
            description = entry.xpath('.//div[@class="formcaddyfab"]//i/b/text()').extract_first()
            size = entry.xpath('.//div[@class="t_size"]/b/text()').extract_first()
            season = entry.xpath('.//div[@class="divformcaddy"]/span/text()').extract_first()
            url = "http://www.gommadiretto.it/cgi-bin/rshop.pl?details=Ordern&typ=" + id
            mydata =  {
                "brand": brand,
                "product_url": url,
                "description": description,
                "id": id,
                "price": price1 + price2,
                "season": season,
                "size": size,
                "source": "gommadiretto.it",
                "ts": ts
            }
            yield scrapy.Request(url, callback=self.parse_tyre, meta={'mydata': mydata})
     
        next_page = response.xpath('//a[@id="ajax_suchergebnisliste_goto_next"]/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_tyre(self, response):
        ean = response.xpath('//div[@id="pdp_tb_info_ean"]//div[@class="pdp_tabC"]/text()').extract_first()
        #description2 = "\n".join(response.xpath('//div[@id="reifendetails_tabs-0"]//text()').extract())
        mydata = response.meta['mydata']
        picture_url = response.xpath('//img[@id="zoom-reifenbild"]/@src').extract_first()
        mydata['ean'] = ean
        #mydata['description2'] = description
        mydata['picture_url'] = response.urljoin(picture_url)

        yield mydata
            
            




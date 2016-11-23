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

class GommadirettoIt(scrapy.Spider):
    name = "gommadirettoit"
    allowed_domains = ["gommadiretto.it"]
    start_urls = ['http://www.gommadiretto.it/cgi-bin/rshop.pl?dsco=130&cart_id=66583165.130.17036&s_p=index']

    def parse(self, response):
        breite = response.xpath('//select[@id="rsmBreite"]/option/text()').extract()
        quer = response.xpath('//select[@id="rsmQuer"]/option/text()').extract()
        felge = response.xpath('//select[@id="rsmFelge"]/option/text()').extract()
        urls = ['http://www.gommadiretto.it/cgi-bin/rshop.pl?s_p=&rsmFahrzeugart=PKW&s_p_=Tutti&dsco=130&tyre_for=&search_tool=&ist_hybris_orig=&with_bootstrap_flag=1&suchen=--Mostrare+tutti+gli+pneumatici--&m_s=3&x_tyre_for=&cart_id=88618236.130.22966&sowigan=&Breite=%s&Quer=%s&Felge=%s&Speed=&Load=&Marke=&kategorie=&filter_preis_von=&filter_preis_bis=&homologation=' % (b, q, f) for b in breite for q in quer for f in felge]
        for u in urls:
             yield scrapy.Request(u, callback=self.parse_tyres)
        
    def parse_tyres(self, response):
        for entry in response.xpath('//div[@class="artikelklotz ajax_artikelklotz ajax_suchergebnisliste_artikelklotz"]'):
            id = entry.xpath('.//a/@name').extract_first()
            brand = entry.xpath('.//div[@class="formcaddyfab"]//font/text()').extract_first()
            price1 = entry.xpath('.//div[@class="price"]//b/text()').extract_first()
            price2 = entry.xpath('.//div[@class="price"]//small/text()').extract_first()
            description = entry.xpath('.//div[@class="formcaddyfab"]//i/text()').extract_first()
            size = entry.xpath('.//div[@class="t_size"]/b/text()').extract_first()
            season = entry.xpath('.//div[@class="divformcaddy"]/span/text()').extract_first()
            url = "http://www.gommadiretto.it/cgi-bin/rshop.pl?details=Ordern&typ=" + id
            # yield scrapy.Request(next_page, callback=self.parse_tyre)
            details =  {
                "brand": brand,
                "description": description,
                "id": id,
                "price": price1 + price2,
                "season": season,
                "size": size,
                "source": "gommadiretto.it"
            }
            request = scrapy.Request(url, callback=self.parse_tyre)
            request.meta['details'] = details
            yield request

    def parse_tyre(self, response):
        ean = response.xpath('//div[@id="pdp_tb_info_ean"]//div[@class="pdp_tabC"]/text()').extract_first()
        description = "\n".join(response.xpath('//div[@id="reifendetails_tabs-0"]//text()').extract())
        details = response.meta['details']
        picture_url = response.xpath('//img[@id="zoom-reifenbild"]/@src').extract_first()
        details['ean'] = ean
        details['description'] = description
        details['picture_url'] = response.urljoin(picture_url)

        yield details
            
            




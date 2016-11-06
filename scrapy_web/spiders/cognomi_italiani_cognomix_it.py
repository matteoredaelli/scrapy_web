# -*- coding: utf-8 -*-
# scrapy  crawl dizionario_italiano_corriere -t jsonlines -o diz.json

import scrapy

class CognomixItalianiSpider(scrapy.Spider):
    name = "cognomi_italiani_cognomix_it"
    allowed_domains = ["cognomix.it"]
    start_urls = (
        'http://www.cognomix.it/origine-cognomi-italiani/A',
        "http://www.cognomix.it/origine-cognomi-italiani/B",
        "http://www.cognomix.it/origine-cognomi-italiani/C",
        "http://www.cognomix.it/origine-cognomi-italiani/D",
        "http://www.cognomix.it/origine-cognomi-italiani/E",
        "http://www.cognomix.it/origine-cognomi-italiani/F",
        "http://www.cognomix.it/origine-cognomi-italiani/G",
        "http://www.cognomix.it/origine-cognomi-italiani/H",
        "http://www.cognomix.it/origine-cognomi-italiani/I",
        "http://www.cognomix.it/origine-cognomi-italiani/J",
        "http://www.cognomix.it/origine-cognomi-italiani/K",
        "http://www.cognomix.it/origine-cognomi-italiani/L",
        "http://www.cognomix.it/origine-cognomi-italiani/M",
        "http://www.cognomix.it/origine-cognomi-italiani/N",
        "http://www.cognomix.it/origine-cognomi-italiani/O",
        "http://www.cognomix.it/origine-cognomi-italiani/P",
        "http://www.cognomix.it/origine-cognomi-italiani/Q",
        "http://www.cognomix.it/origine-cognomi-italiani/R",
        "http://www.cognomix.it/origine-cognomi-italiani/S",
        "http://www.cognomix.it/origine-cognomi-italiani/T",
        "http://www.cognomix.it/origine-cognomi-italiani/U",
        "http://www.cognomix.it/origine-cognomi-italiani/V",
        "http://www.cognomix.it/origine-cognomi-italiani/W",
        "http://www.cognomix.it/origine-cognomi-italiani/X",
        "http://www.cognomix.it/origine-cognomi-italiani/Y",
        "http://www.cognomix.it/origine-cognomi-italiani/Z",
    )

    def parse(self, response):
        words = response.xpath('//div[@class="contenuto"]//li/a/text()').extract()
        for word in [s.replace(" -  Origine del Cognome","") for s in words]:
            yield { "cognome": word.replace(" -  Origine del Cognome",""), "source": "cognomix.it"}
            
        # extracting next pages
        for next_page in response.xpath('//div[@class="text-center"]/a/@href').extract():
            if next_page is not None and next_page != "#":
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)




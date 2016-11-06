# -*- coding: utf-8 -*-
# scrapy  crawl dizionario_italiano_corriere -t jsonlines -o diz.json

import scrapy

class DizionarioItalianoCorriereSpider(scrapy.Spider):
    name = "dizionario_italiano_it"
    allowed_domains = ["dizionario-italiano.it"]
    start_urls = (
        'http://dizionario-italiano.it/dizionario-italiano.php?browse=A',
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=B",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=C",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=D",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=E",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=F",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=G",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=H",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=I",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=J",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=K",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=L",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=M",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=N",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=O",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=P",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=Q",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=R",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=S",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=T",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=U",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=V",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=W",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=X",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=Y",
        "http://dizionario-italiano.it/dizionario-italiano.php?browse=Z",

    )

    def parse(self, response):
        for row in response.xpath('//td[@class="br_italiano"]/a'):
            word = row.xpath('text()').extract_first()
            gramma = row.xpath('span//i/text()').extract_first()
            yield { "word": word.strip(), "gramma": gramma, "source": "dizionario-italiano.it"}
            
            # extracting next pages
            next_page = response.xpath('//td[@id="pag"][2]/a/@href').extract_first()
            if next_page is not None and next_page != "#":
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)




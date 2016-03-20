# -*- coding: utf-8 -*-
import scrapy
from scraper_103_by.items import Scraper103ByItem
import logging

class GrodnenskoeRupPharmaciaPharmacySpider(scrapy.Spider):
    name = "grodnenskoe_rup_pharmacia_pharmacy"
    allowed_domains = ["apteka.103.by"]

    # номера аптек гродненского РУП 
    # в нотации 103.by
    gr_ph_nums    = ["1",     "106",    "109",    "110",    "113",    "114", 
                     "84",    "89"      "119",    "124",    "131",    "134", 
                     "135",   "143",    "145",    "147",    "149",    "150", 
                     "152",   "153",    "157",    "158",    "159",    "160", 
                     "164",   "170",    "174",    "175",    "18",     "180", 
                     "186",   "188",    "19",     "190",    "195",    "199", 
                     "2",     "200",    "203",    "205",    "215",    "220", 
                     "221",   "223",    "230",    "232",    "3",      "36",  
                     "43",    "49",     "63",     "79",     "131_nochnoy",  
                     "114_nochnoy"]
    # for debug
    #gr_ph_nums    = ["1"]
    
    url_tmplt = u'http://www.apteka.103.by/pharmacies/grodnenskoe_rup_pharmacia_pharmacy_%s'
    
    # Адреса первых страниц списков товаров аптек
    start_urls = [url_tmplt % (num,) for num in gr_ph_nums] 

    traversed = []

    def parse(self, response):

        # сбор собственно данных
        curr_apt = response.xpath('//h1[@class="title02"]/text()').extract()[0].strip()
        #logging.warning(curr_apt)
        for tr in response.xpath('//table[@class="table02"]/tr'):
            curr_item = Scraper103ByItem()
            curr_item["source"]         = curr_apt        
            curr_item["asset"]          = tr.xpath('td[@class="th01"]/span[@class="link"]/text()').extract()[0].strip()         
            curr_item["manufacturer"]   = tr.xpath('td[@class="th01"]/span[@class="name"]/text()').extract()[0].strip()            
            curr_item["quant"]          = tr.xpath('td[@class="th03"]/strong/text()').extract()[0].strip()           
            curr_item["price"]          = tr.xpath('td[@class="th04"]/span[@class="price"]/text()').extract()[0].strip()
            yield curr_item

        # обработка пагинаций 
        curr_pg = response.xpath('//div[@class="pager line"]/a[@class="current"]/@href').extract()[0].strip()
        if curr_pg not in self.traversed:
          self.traversed.append(curr_pg)

        for pg in response.xpath('//div[@class="pager line"]/a/@href').extract():
          if pg.strip() not in self.traversed:
            self.traversed.append(pg.strip())
            yield scrapy.http.Request('http://apteka.103.by%s' % (pg,))

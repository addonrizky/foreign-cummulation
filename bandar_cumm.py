import scrapy
from scrapy.http import FormRequest
import mysql.connector
from mysql.connector import errorcode
from constant_emiten_url import start_urls
from utility import *
from model import * 
from time import sleep


class QuotesSpider(scrapy.Spider):
    name = "cummulationlcrawler"
    start_urls = start_urls

    def parse(self, response):
        #retrieve emiten code
        emiten_tag = response.css("div.mb10 > ul.breadcrumb > h5::text")
        emiten_text = emiten_tag.get()

        list_brokersum_url = {}

        #compose list of url broker summary of the emiten, for 20 days
        list_brokersum_url = Utility.get_past_working_day(20, emiten_text)

        print(list_brokersum_url)


        for key in list_brokersum_url:
            #print(key, '->', list_brokersum_url[key])
            yield scrapy.Request(list_brokersum_url[key], self.broker_summary,  meta={'past_day': key, 'url' : list_brokersum_url[key]})


    def broker_summary(self, response):
        #retrieve emiten code
        emiten_url = response.request.url
        kode_saham = emiten_url[77:81]

        whole_table = response.css("table.table-summary > tfoot > tr > th > div > span.ml5")
        foreign_netval = whole_table[1].css("::text").get()[10:]
        
        foreign_netval = Utility.convert_string_amount(foreign_netval)
        
        field_to_save = "foreign_netval_"+str(response.meta['past_day'])+"dago"
        value_to_save = foreign_netval

        the_model = Model()
        #sleep(1)
        the_model.save(field_to_save, value_to_save, kode_saham)
        print("hmmmm")
        
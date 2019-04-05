# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class CartaCapitalSpider(scrapy.Spider):
    name = 'carta_capital'
    allowed_domains = ['cartacapital.com.br']
    start_urls = []

    def __init__(self, *a, **kw):
        super(CartaCapitalSpider, self).__init__(*a, **kw)
        with open('frontier/carta_capital.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        urls = [a.attrib['href'] for a in response.css('h3.eltdf-pt-three-title > a')]

        for url in urls:
            yield scrapy.Request(url, self.parse1)
    
    def parse1(self, response):
        def getDateTime(date):
            return date
        def getText(text):
            return text

        title = response.css('h1.eltdf-title-text::text').get()
        section = response.url.split("/")[-3]
        sub_title = response.css('div.wpb_text_column > div.wpb_wrapper > h3::text').get()
        author = response.css('a.eltdf-post-info-author-link::text').get()
        date = getDateTime(response.css('div.eltdf-post-info-date > a::text').get())
        text = getText(response.css('div.eltdf-post-text-inner').get())

        yield {
            'title': title,
            'sub_title': sub_title,
            'author': author,
            'date': date,
            'section': section,
            'text': text,
            'url': response.url
        }

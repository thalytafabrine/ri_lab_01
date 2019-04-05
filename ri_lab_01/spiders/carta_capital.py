# coding: utf-8
import scrapy
import json

from datetime import datetime
from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class CartaCapitalSpider(scrapy.Spider):
    name = 'carta_capital'
    allowed_domains = ['cartacapital.com.br']
    start_urls = []
    # URLs já visitadas
    urls = []

    def __init__(self, *a, **kw):
        super(CartaCapitalSpider, self).__init__(*a, **kw)
        with open('frontier/carta_capital.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())
    
    def getDateTime(self, response):
        return response.css('div.eltdf-post-info-date > a::text')
    
    def isValidDate(self, response):
        date = response.css('div.eltdf-post-info-date a::attr(href)').get().split("/")[-3]
        return int(date) >= 2018
    
    def isLinkCartaCapital(self, link):
        for section in self.start_urls:
            if (section.lower() in link.lower()):
                return True
        return False

    def isValidArticle(self, link):
        if ((link is not None) and self.isLinkCartaCapital(link) and (self.urls.count(link) == 0)):
            return True
        return False

    def parse(self, response):
        if(self.isValidDate(response)):
            yield self.getArticleData(response)

        for nextpage in response.css('a::attr(href)').getall():
            if (self.isValidArticle(nextpage)):
                yield scrapy.Request(nextpage, self.parse)
            self.urls.append(nextpage)

    def getArticleData(self, response):

        def getSection():
            return response.xpath("//meta[@property='article:section']/@content").get()

        def getText():
            return "".join(response.css('article p::text').getall())

        title = response.css('h1.eltdf-title-text::text').get()
        sub_title = response.css('div.wpb_text_column > div.wpb_wrapper > h3::text').get()
        author = response.css('a.eltdf-post-info-author-link::text').get() 

        articleData = {
            'title': title,
            'sub_title': sub_title,
            'author': author,
            'date': self.getDateTime(response),
            'section': getSection(),
            'text': getText(),
            'url': response.url
        }

        return articleData

import scrapy


class DomisiliItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()

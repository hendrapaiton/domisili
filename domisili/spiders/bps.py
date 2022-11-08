import scrapy


class BpsSpider(scrapy.Spider):
    name = 'bps'
    allowed_domains = ['sig.bps.go.id']
    start_urls = ['https://sig.bps.go.id/bridging-kode/index']

    def parse(self, response):
        pass

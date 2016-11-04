import scrapy


class Spider_1800(scrapy.Spider):
    name = 'contractor'
    allowed_domains = ['1800contractor.com']
    start_urls = (
        'http://www.1800contractor.com/d.Atlanta.GA.html?link_id=3658',
    )

    def parse(self, response):
        urls = response.xpath('/html/body/center/table/tr/td[2]/table/tr[6]/td/table/tr[2]/td/b/a/@href').extract()

        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_contractors)
            yield request

        # process next page

        next_page_url = response.xpath('/html/body/div[1]/center/table/tr[8]/td[2]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_contractors(self, response):
        name = response.xpath(
            '/html/body/div[1]/center/table/tr[5]/td/table/tr[1]/td/b/a/@href').extract()
        contrator = {
           'name': name,

            'url': response.url}
        yield contrator
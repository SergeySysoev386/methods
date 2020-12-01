import scrapy
from scrapy.http import HtmlResponse
from read.items import ReadItem


class LabSpider(scrapy.Spider):
    name = 'lab'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%8F/?stype=0']

    def parse(self, response: HtmlResponse):
        books = response.xpath("//a[@class='product-title-link']/@href").extract()
        for link in books:
            yield response.follow(link, callback=self.book_parse)

        next_page = response.xpath(
            "//a[@title='Следующая']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def book_parse(self, response: HtmlResponse):
        link = response.xpath("//link[@rel='canonical']/@href").extract()
        title = response.xpath("//h1/text()").extract_first()
        author = response.xpath("//a[@data-event-label='author']//text()").extract()
        full_price = response.xpath("//span[@class='buying-priceold-val-number']//text()").extract()
        discount = response.xpath("//span[@class='buying-pricenew-val-number']//text()").extract()
        rating = response.xpath("//div[@id='rate']//text()").extract()
        yield ReadItem(
            item_title=title, item_author=author, item_full_price=full_price, item_discount=discount,
            item_link=link, item_rating=rating)

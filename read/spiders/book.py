import scrapy
from scrapy.http import HtmlResponse
from read.items import ReadItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%BD%D0%BE%D0%BC%D0%B8%D1%8F']

    def parse(self, response: HtmlResponse):

        books = response.xpath("//a[@class='book-preview__title-link']/@href").extract()
        for link in books:
            yield response.follow(link, callback=self.book_parse)

        next_page = response.xpath("//*[normalize-space(text()) = 'Далее']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        else:
            return

    def book_parse(self, response: HtmlResponse):
        link = response.xpath("//link[@rel='amphtml']/@href").extract()
        title = response.xpath("//h1[@class='item-detail__title']/text()").extract_first()
        author = response.xpath("//a[@itemprop='author']//text()").extract()
        full_price = response.xpath("//div[@class='item-actions__price-old']//text()").extract()
        discount = response.xpath("//b[@itemprop='price']//text()").extract()
        rating = response.xpath("//span[@class='rating__rate-value']//text()").extract()
        yield ReadItem(
            item_title=title, item_author=author, item_full_price=full_price, item_discount=discount,
            item_link=link, item_rating=rating)

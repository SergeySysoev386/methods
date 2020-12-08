from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from read.spiders.lab import LabSpider
from read.spiders.book import BookSpider
from read import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabSpider)
    process.crawl(BookSpider)

    process.start()
import os
import sys

import scrapy
from scrapy.crawler import CrawlerProcess

# sys.path.insert(1, '/c/Users/lynns/coding/corners/map-tv-data/tvscraper/tvscraper')
# from tvscraper import TvspiderSpider

sys.path.append(os.path.join(os.path.abspath('../')))
from tvscraper.tvscraper.spiders.tvspider import TvspiderSpider


# 1. use web crawler to get identifiers of videos with the keyword "shooting" from tv news archive
# os.system('cd tvscraper & scrapy crawl tvspider -o {file}'.format(
#     file = './testing.csv'
# ))
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(TvspiderSpider, start="2023-08-12", end="2023-08-12")
process.start() # the script will block here until the crawling is finished


# 2. download metadata and HTML files for all identifiers



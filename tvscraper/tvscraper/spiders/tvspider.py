import scrapy
from scrapy.http.request import Request
from scrapy.exceptions import CloseSpider

import re

class TvspiderSpider(scrapy.Spider):
    name = "tvspider"
    allowed_domains = ["archive.org"]

    #root_url = "https://archive.org/details/tv?q=(shooting)%20AND%20collection:(tvarchive)%20AND%20date:[2022-02-01%20TO%202022-03-01]%5D&page="
    #root_url = "https://archive.org/details/tv?q=%28zendaya%29+AND+collection%3A%28tvarchive%29+AND+date%3A%5B2020-01-01+TO+2020-10-01%5D&page="
    root_url = "https://archive.org/details/tv?q=%28shooting%29%20AND%20collection%3A%28tvarchive%29%20AND%20date%3A%5B2021-03-01%20TO%202021-03-08%5D&page="
    page_num = 1
    start_urls = []

    url = root_url + str(page_num)
    start_urls.append(url)

    def parse(self, response):
        # check whether page has results
        main_container = response.selector.xpath('//*[@id="maincontent"]/div[3]')[0].get()
        if "search-fail" in main_container:
            raise CloseSpider('no more results')
        else:
            self.page_num += 1

        videos = response.selector.xpath('//*[@id="ikind-search"]/div/div')
        #video_hlinks = videos.xpath('//*[@id="ikind-search"]/div/div/div/div[1]/a')
        video_hlinks = videos.css('div.item-ttl a')
        for hlink in video_hlinks:
            link = hlink.attrib['href']

            # get identifier
            pattern = '([A-Z])\\w+'
            identifier = re.search(pattern, link).group()

            yield {
                #'link': hlink.attrib['href']
                'identifier': identifier
            }
            
        next_page = self.root_url + str(self.page_num)
        yield Request(next_page)

# videos = response.selector.xpath('//*[@id="ikind-search"]/div/div') <-- includes the hidden news channel link elements
# video_links = videos.xpath('//*[@id="ikind-search"]/div/div/div/div[1]/a') <-- video link elements 
# videos.xpath('//*[@id="ikind-search"]/div/div/div/div[1]/a') <-- link but only for the first item
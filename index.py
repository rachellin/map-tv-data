import os
import sys
import subprocess
sys.path.append(os.path.join(os.path.abspath('../')))

import scrapy
from scrapy.crawler import CrawlerProcess
from tvscraper.tvscraper.spiders.tvspider import TvspiderSpider

# import scripts.scrape_archive_org_copy as scrape_archive_org
# import scripts.parse_archive_new_copy as parse_archive_new

from segment_vids import *


# 1. use web crawler to get identifiers of videos with the keyword "shooting" from tv news archive
# os.system('cd tvscraper & scrapy crawl tvspider -o {file}'.format(
#     file = './testing.csv'
# ))
# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })

# process.crawl(TvspiderSpider, start="2023-08-12", end="2023-08-12", outfile="aug-12-2023") # TODO get command line inputs 
# process.start() # the script will block here until the crawling is finished


# 2. download metadata and HTML files for all identifiers
subprocess.run(["py", "scripts/scrape_archive_org.py", "--meta", "meta-aug12", "--html", "html-aug12", "aug-12-2023.csv"], shell=True)

# 3. parse and extra meta fields and transcripts
subprocess.run(["py", "scripts/parse_archive_new.py", "-o", "aug-12-2023-out.csv", "--meta", "meta-aug12", "--html", "html-aug12", "aug-12-2023.csv"], shell=True)

# 4. segment videos for relevant minutes
# grouped_videos = group_videos('./data/june-2022-week.csv')
# get_segments(grouped_videos)        
# slice_csv(grouped_videos, "./data/june-2022-week-sliced.csv", "segment_vids.json")
# filter_videos("./data/june22-sliced.csv")
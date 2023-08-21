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
from clean_text import clean_text

import time
start = time.time()

# 1. use web crawler to get identifiers of videos with the keyword "shooting" from tv news archive
# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })

# process.crawl(TvspiderSpider, start="2022-01-01", end="2022-12-31", outfile="2022-identifiers") # TODO get command line inputs 
# process.start() # the script will block here until the crawling is finished


# 2. download metadata and HTML files for all identifiers
# subprocess.run(["py", "scripts/scrape_archive_org.py", "--meta", "data/meta-2022", "--html", "data/html-2022", "2022-identifiers.csv"], shell=True)

# 3. parse and extra meta fields and transcripts
# subprocess.run(["py", "scripts/parse_archive_new.py", "-o", "data/2022.csv", "--meta", "data/meta-2022", "--html", "data/html-2022", "2022-identifiers.csv"], shell=True)

# 4. segment videos for relevant minutes
# grouped_videos = group_videos('./data/2022.csv')
# get_segments(grouped_videos, "./data/2022-segments.json")        
# slice_csv(grouped_videos, "./data/2022-sliced.csv", "./data/2022-segments.json")

# 5. tokenize
clean_text("./data/2022-sliced.csv", "./data/2022-tokenized.csv")

end = time.time()
print("The time of execution of above program is :",
      (end-start) / 60, "mins")


''' 2022 whole year execution times
step 1. 22 mins (except i accidentally uncommented the os one too)
step 2.
step 3. 71 mins
step 4. 12 mins
step 5. 25 mins
'''



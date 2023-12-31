#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import optparse
#import csv
import pandas as pd

import gzip
import time
#import xml.parsers.expat

import requests

#from bs4 import BeautifulSoup
import concurrent.futures
import logging
import os

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler("logs/scrape_archive_org.log"),
                              logging.StreamHandler()])

__version__ = 'r5 (2022/10/28)'

META_DIR = 'data/meta/'
HTML_DIR = 'data/html/'
MAX_WORKERS = int(os.environ.get("MAX_WORKERS", 3))



def parse_command_line(argv):
    """Command line options parser for the script
    """
    usage = "Usage: %prog [options] <CSV input file>"

    parser = optparse.OptionParser(usage=usage)
    parser.add_option("--meta", action="store",
                      type="string", dest="meta", default=META_DIR,
                      help="Meta files directory (default: '{:s}')".format(META_DIR))
    parser.add_option("--html", action="store",
                      type="string", dest="html", default=HTML_DIR,
                      help="HTML files directory (default: '{:s}')".format(HTML_DIR))
    parser.add_option("-s", "--skip", action="store",
                      type="int", dest="skip", default=0,
                      help="Skip rows (default: 0)")
    parser.add_option("-c", "--compress", action="store_true",
                      dest="compress", default=False,
                      help="Compress downloaded files (default: No)")

    return parser.parse_args(argv)


def download_file(options, url, local_filename):
    # NOTE the stream=True parameter
    logging.info("Downloading...[{:s}]".format(url))

    r = requests.get(url, stream=True)
    if options.compress:
        f = gzip.open(local_filename, 'wb')
    else:
        f = open(local_filename, 'wb')

    for chunk in r.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
            f.flush()
    f.close()


def handle_download(_id, retry=0):
    try:
        _id = _id[0]
        file_name = os.path.join(options.meta, _id + "_meta.xml")

        if options.compress:
            file_name += ".gz"

        if not os.path.isfile(file_name):
            rq = requests.get('http://archive.org/download/' + _id)
            if rq.status_code == 200:
                if not rq.url.endswith('/'):
                    rq.url = rq.url + '/'
                
                url = rq.url + _id + "_meta.xml"
                if not os.path.isfile(file_name):
                    download_file(options, url, file_name)

        url = 'http://archive.org/details/' + _id
        file_name = os.path.join(options.html, _id + ".html")

        if options.compress:
            file_name += ".gz"
        if not os.path.isfile(file_name):
            download_file(options, url, file_name)
    except:
        if retry > 4:
            logging.error(f'id: {_id}. Stopped retrying')

        else:
            retry += 1
            wait_time = 120
            logging.warning(f'id: {_id}. Waiting {wait_time} secs and retrying... ')
            time.sleep(wait_time)
            handle_download(_id, retry=retry)


def parallel_download(identifiers):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for r in executor.map(handle_download, identifiers):
            if r:
                logging.warning(r)


if __name__ == "__main__":
    logging.info("{:s} - {:s}\n".format(os.path.basename(sys.argv[0]), __version__))
    logging.info(f'Max workers set to {MAX_WORKERS}')

    (options, args) = parse_command_line(sys.argv)
    if len(args) < 2:
        logging.info("Usage: {:s} [options] <CSV input file>".format(os.path.basename(sys.argv[0])))
        sys.exit(-1)

    if not os.path.exists(options.meta):
        os.mkdir(options.meta)

    if not os.path.exists(options.html):
        os.mkdir(options.html)

    # CSV to list
    df = pd.read_csv(args[1])
    identifiers = [list(row) for row in df.values]

    # Consider skip option
    if options.skip:
        identifiers = identifiers[options.skip:]
    
    # Download
    if os.environ.get("ARCHIVE_TEST"):
        # Testing
        for id_ in identifiers:
            handle_download(id_)
    else:
        # Multithread
        total = len(identifiers)
        logging.info(f'{total} total identifiers to process...')
        downloaded = len(os.listdir(options.html))
        logging.info(f'{downloaded} total identifiers downloaded...')
        while downloaded < total:
            try:
                parallel_download(identifiers)
            except Exception as e:
                logging.warning(f'Restarting: {e}')
            
            time.sleep(120)

    logging.info("All done")

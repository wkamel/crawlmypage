"""
Module for simulating many users activity on website.
"""
import sys
import random
import logging
import time
from datetime import datetime
from crawler import Crawler
from helpers import get_random_time, load_user_agents, get_proxies

logging.basicConfig(level=logging.INFO)

MAX_THREADS = 10


class App(object):
    user_agents = []

    def __init__(self):
        self.crawlers = []
        # filepath = 'data/useragents.txt'
        # self.user_agents = load_user_agents(filepath)

    def start(self, url):
        proxies = []

        while True:
            logging.info("Length on proxies %d" % (len(proxies)))
            if len(proxies) == 0:
                logging.info("load new proxies")                
                proxies = get_proxies()

            if not self.is_crawlers_limit():
                # load proxy
                proxy = proxies.pop()
                crawler = Crawler(url, proxy)
                self.crawlers.append(crawler)
                crawler.start()           
            time.sleep(5)

    def is_crawlers_limit(self):
        """
        Update list of crawlers by eliminating non-alive threads
        returns:
            boolean - True if no f crawlers excceed the  MAX_THREADS limit
        """
        crawlers = []
        for crawler in self.crawlers:
            if crawler.is_alive():
                crawlers.append(crawler)

        logging.info("no of crawlers %d " % len(self.crawlers))
        self.crawlers = crawlers
        if len(self.crawlers) >= MAX_THREADS:
            return True
        else:
            return False


if __name__ == '__main__':
    app = App()
    args = sys.argv
    if len(args) == 2:
        website_url = args[1]
        app.start(website_url)

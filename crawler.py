import sys
import requests
import random
import threading
from selenium import webdriver
from datetime import datetime
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)


class CrawlerThreadTimeoutException(Exception):
    pass


class CrawlerCantOpenPageException(Exception):
    pass


class Crawler(threading.Thread):

    def __init__(self, url, proxy):
        threading.Thread.__init__(self) 
        self.url = url
        self.proxy = proxy
        self.d = None
        self.init_browser()

    def run(self):
        self.set_time_info()
        logging.info("Start crawler with proxy %s " % (self.proxy))
        try:  
            self.open_page()
        except Exception as ex:
            logging.error(str(ex))
            self.d.quit()

    def open_page(self, lasturl=False):
        self.try_close()
        if lasturl:
            self.wait()
            url = self.get_url(lasturl)
            # logging.info("Click on link")
            # logging.info(url)
            # link = self.d.find_element_by_xpath("//a[@href='%s']" % (url))            
            # link.click()            
        else:
            url = self.url        
        logging.info("url %s", url)        
        self.d.get(url) 
        try:            
            element = self.d.find_element_by_xpath("//footer[@id='footer']")
        except:
            logging.info("After")
            raise CrawlerCantOpenPageException("Element footer not found on page")        

        self.open_page(lasturl=url)        


    def get_url(self, lasturl):
        urls = [el.get_attribute('href') for el in self.d.find_elements_by_xpath("//a")]
        valid_urls = list(filter(lambda url: url.startswith(self.url) and url != lasturl, urls))
        url = random.choice(valid_urls)
        # url = url.replace(self.url, "")
        logging.info("Random url:%s" % url)
        return url

    def set_time_info(self):
        """ set start time and celect random value of spider working time """
        self.start_time = datetime.now()
        self.life_time = random.randint(250, 500)
        logging.info("Crawler lifetime %d" % (self.life_time))

    def try_close(self):
        if (datetime.now() - self.start_time).seconds >= self.life_time:
            logging.info("Spider life time expired %s" % (self.life_time))            
            raise CrawlerThreadTimeoutException("Thread terminated after %d " % (self.life_time))

    def wait(self):
        secs = random.randint(60, 100)
        logging.info("::Sleeping for %s" % secs)
        time.sleep(secs)

    def init_browser(self):
        if self.proxy:
            webdriver.DesiredCapabilities.CHROME['proxy'] = {
                "httpProxy":self.proxy,
                "ftpProxy":self.proxy,
                "sslProxy":self.proxy,
                "noProxy":None,
                "proxyType":"MANUAL",
                "class":"org.openqa.selenium.Proxy",
                "autodetect":False
                }
        self.d = webdriver.Chrome()
        self.d.set_page_load_timeout(8)
        self.d.set_window_size(0, 0)


    def set_headers(self, user_agent):
    
        self.heades = {
            'User-Agent': user_agent,
        }


if __name__ == '__main__':
    url = "https://softarm.pl"
    crawler = Crawler(url, None)
    crawler.run()


"""
Helper functions for crawler app
"""

from datetime import datetime 
import random
import logging
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_random_time():
    now = datetime.now()
    random.seed(datetime.now())
    seconds = random.randint(20, 300)
    return seconds


def load_user_agents(filepath):
    user_agents = []
    with open(filepath) as filepointer:
        for  line in filepointer.readlines():
            agent = line[0:-2]
            user_agents.append(agent)

    logging.info("%d user agents laoded" % len(user_agents))
    return user_agents

def get_proxies():
    proxy_urls = [] 
    # url = "https://hidemy.name/en/proxy-list/"
    url = "https://hidemy.name/en/proxy-list/?country=BYCACZDEGRHUIELTLUMKMDNLNOPLPTRURSSKSIESSECHTRUAGBUS&type=s&anon=34#list"
    d = webdriver.Chrome()
    d.get(url)
    try:
        element = WebDriverWait(d, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "proxy__t"))
        )
    except Exception as Ex:
        print(Ex)
        print('exit')
        d.quit()
        return []

    rows = d.find_elements_by_xpath("//table[@class='proxy__t']/tbody/tr")
    for row in rows:
        tds = row.find_elements_by_xpath("./td")
        url = tds[0].text
        port = tds[1].text
        proxy_urls.append("{}:{}".format(url, port))
    d.quit()
    return proxy_urls

from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time
import random
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

#creates connection to mongodb database table
client = pymongo.MongoClient()
db = client.zillow
pages = db.main_pages


def getData():
    '''
    Scrape entire webpage content and load to mongodb database
    '''
    zillow_url = 'https://www.zillow.com/austin-tx/?searchQueryState={%22pagination%22:{%22currentPage%22:1},%22mapBounds%22:{%22west%22:-98.2917712392578,%22east%22:-97.27965576074217,%22south%22:29.89352113750375,%22north%22:30.69272360583364},%22regionSelection%22:[{%22regionId%22:10221,%22regionType%22:6}],%22isMapVisible%22:true,%22filterState%22:{},%22isListVisible%22:true}'
    browser.visit(zillow_url)
    html = browser.html
    soup = bs(html,'html.parser')
    pag = soup.find_all(class_="search-pagination")
    lst_num = re.findall(r'\d+',pag[0].get_text().split('.')[-1])[0]
    for pg in range(1,int(lst_num)+1):
        if pg < int(lst_num):
            html = browser.html
            soup = bs(html,'html.parser')
            pages.insert_one({'html': html, 'time_scraped': time.ctime()})
            time.sleep(random.randint(5,25))
            browser.links.find_by_partial_text('NEXT')
        else:
            html = browser.html
            soup = bs(html,'html.parser')
            pages.insert_one({'html': html, 'time_scraped': time.ctime()})

browser.quit()

if __name__ == '__main__':
    getData()
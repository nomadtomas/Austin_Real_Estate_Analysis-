from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time
import random
from splinter import Browser
from selenium import webdriver

executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)#, headless= False)

client = pymongo.MongoClient()
db = client.realtor
pages = db.main_pages

realtor_url = "https://www.realtor.com/realestateandhomes-search/Austin_TX/pg-"

def realtorScrape():
    browser.visit(realtor_url)
    html = browser.html
    soup = bs(html,'html.parser')

    #obtain the last page of the website
    pag = soup.find_all(class_="pagination")
    lst_num = pag[0].get_text(strip=True)[-2:]


    for x in range(1,int(lst_num)+1):
        response = browser.visit(realtor_url + str(x))
        html = browser.html
        soup = bs(html,'html.parser')
        pages.insert_one({'html': html, 'time_scraped': time.ctime()})    
        time.sleep(random.randint(5,30))

    message = 'Pages scraped: {}'.format(lst_num)
    return message

if __name__ == '__main__':
    realtorScrape()
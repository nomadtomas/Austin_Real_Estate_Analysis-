from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time

client = pymongo.MongoClient()
db = client.realtyaus
pages = db.main_pages

def ausrealtyScrape():
    '''
    Scrape entire webpage content and load to mongodb database
    '''
    #establish url to scrape
    realtyaus_url = "https://www.realtyaustin.com/austin-home-search.php?p="
    response = requests.get(realtyaus_url)
    soup = bs(response.text, 'html.parser')

    #find last page of the website with data
    pag = soup.find_all(class_='pagination')
    lst_num = pag[1].get_text().split()[-2]
    #set lst_num to an int
    lst_num = int(lst_num)

    for n in range(1, lst_num+1):
        response = requests.get(realtyaus_url + str(n))
        soup = bs(response.text, 'html.parser')
        pages.insert_one({'html': response.content, 'time_scraped': time.ctime()})    
    return print("Finished Scraping Data: of {} pages".format(lst_num))
if __name__ == '__main__':
    ausrealtyScrape()
import pandas as pd
import numpy as np
import pymongo
from bs4 import BeautifulSoup as bs
import time
import re


def realtor_df(collection):
    df = pd.DataFrame(list(collection.find()))
    data= df[['html', 'time_scraped']]

    dataframe = []
    badlinks = []

    for x in data['html']:
        try:
            dt = conver_data(x)
            dt['time'] = data['time_scraped']
            dataframe.append(dt)
        except:
            badlinks.append(df['_id'])
            pass

    total_df = pd.concat(dataframe)
    total_df.reset_index(drop=True, inplace=True)
    realtor_df = clean_df(total_df)
    return realtor_df
    
def conver_data(data):
    
    soup = bs(data, 'html.parser')
    listings = soup.find_all(class_='srp-body')
    address = [x.get_text().split('\n')[2].strip() for x in listings[0].find_all(class_='seo-wrap hide')]
    city = [x.get_text().split('\n')[3].strip() for x in listings[0].find_all(class_='seo-wrap hide')]
    state = [x.get_text().split('\n')[4].strip() for x in listings[0].find_all(class_='seo-wrap hide')]
    zipcode = [x.get_text().split('\n')[5].strip() for x in listings[0].find_all(class_='seo-wrap hide')]
    data_type = [x.get_text(strip=True) for x in listings[0].find_all(class_='property-type')]
    prices = [x.get_text(strip=True) for x in listings[0].find_all(class_='data-price')]
    productId = [x.select('meta')[2]['content'] for x in listings[0].find_all(class_='price ab-price')]
    listingId = [x['data-listingid'] for x in listings[0].find_all(class_="component_property-card js-component_property-card js-quick-view")]
    beds = [x.select('li')[0].get_text(strip=True) for x in listings[0].find_all(class_='prop-meta ellipsis ab-prop-meta')]
    baths = [x.select('li')[1].get_text(strip=True) for x in listings[0].find_all(class_='prop-meta ellipsis ab-prop-meta')]
    sqft = [x.select('li')[2].get_text(strip=True) for x in listings[0].find_all(class_='prop-meta ellipsis ab-prop-meta')]
    details_links = [x.a['href'] for x in listings[0].find_all(class_="location-wrapper-relative ab-location-display")]
    lat = [x.select('meta')[0]['content'] for x in listings[0].find_all(class_='listing-geo')]
    lon = [x.select('meta')[1]['content'] for x in listings[0].find_all(class_='listing-geo')]
    photos = [x.img['src'] for x in listings[0].find_all(class_='photo-wrap')]
    
    data = {
        'address': address,
        'city': city,
        'state': state,
        'zip': zipcode,
        'data_type': data_type,
        'price': prices,
        'productId': productId,
        'listingId': listingId,
        'beds': beds,
        'baths': baths,
        'sqft': sqft,
        'details_links':details_links,
        'lat': lat,
        'lon': lon,
        'photos': photos
    }
    
    df = pd.DataFrame([pd.Series(value, name=k) for k, value in data.items()]).T
    
    return df

def clean_df(total_df):
    total_df['cost'] = total_df['price'].str.replace(r'\D', '').astype('float')
    total_df['beds'] = total_df['beds'].str.replace(r'[a-zA-Z]', '').astype('float')
    total_df['baths'] = total_df['baths'].str.replace(r'[a-zA-Z+]', '').astype('float')
    total_df['sq_ft'] = total_df['sqft'].str.replace(r'[a-zA-Z,]', '').astype('float')
    total_df['lat'] = pd.to_numeric(total_df['lat'], errors='coerce')
    total_df['lon'] = pd.to_numeric(total_df['lon'], errors='coerce')
    total_df['time'] = pd.to_datetime(total_df['time'])
    total_df['source'] = 'reator'

    col = ['price', 'sqft']
    total_df.drop(col, axis=1, inplace=True)

    return total_df




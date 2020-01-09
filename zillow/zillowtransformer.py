import pandas as pd
import numpy as np
import pymongo
from bs4 import BeautifulSoup as bs
import time
import re


def zillow_df(collection):
    '''
    Iterates through row objects applying the convert_data function to strip data of html and xlm objects

    Parameters:
    -----------
    collection (mongodb connection): connection to db to extract data to be converted

    Returns:
    --------
    Dataframe:
        Processed dataframe of real estate parameters 
    '''

    #retrieved data from mongo into a dataframe
    df = pd.DataFrame(list(collection.find()))
    data = df[['html', 'time_scraped']]

    dataframe = []
    badlinks = []
    for x in data['html']:
        try:
            dt = convert_data(x)
            dt['time'] = data['time_scraped']
            dataframe.append(dt)
        except:
            badlinks.append(df['_id'])
            pass

    total_df = pd.concat(dataframe)
    total_df.reset_index(drop=True, inplace=True)
    zillow_df = clean_df(total_df)
    return zillow_df

def convert_data(data):
    '''
    Convert html data from realtyaus database into dataframe by obtaining key elements from 
    each webpage.
    
    Parameters:
    -----------
    data (dataframe): html object data

    Returns:
    --------
    Dataframe: df of housing parameters of mlsid, subdiv, address, loc, bed, bath, 
    sqft, acre, dtype, price, status, statusext, photo
    '''
    
    #initiate beautiful soup html.parser
    soup = bs(data, 'html.parser')

    #utilized find_all to obtain elements location
    listings = soup.find_all(class_='photo-cards photo-cards_wow photo-cards_short')

    prices = [x.get_text(strip=True) for x in listings[0].find_all(class_='list-card-price')]
    days_on_zillow = [x.select('div')[0].get_text(strip=True) for x in listings[0].find_all(class_='list-card-top')]
    lat_lon = [x.get_text() for x in listings[0].find_all('script')]
    addresses = [x.get_text(strip=True) for x in listings[0].find_all(class_='list-card-addr')]
    details =[x.get_text().split() for x in listings[0].find_all(class_='list-card-details')]
    data_type =[x.get_text(strip=True) for x in listings[0].find_all(class_='list-card-type')]
    links = [x.a['href'] for x in listings[0].find_all(class_='list-card-top')]
    
    #create a dictionary 
    data = {
        'details': details,
        'location': addresses,
        'data_type': data_type,
        'price': prices,
        'links': links,
        'days_on':days_on_zillow,
        'lat_lon':lat_lon
    }
    
    #convert dictionary into pandas dataframe, used pd.Series to assure all parameter lengths are equal
    df = pd.DataFrame([pd.Series(value, name=k) for k, value in data.items()]).T
    df = df.dropna(subset=['location'])
    return df

def clean_df(total_df):
    '''
    Updates dataframe data types
    
    Parameters:
    -----------
    data (dataframe): real estate columns to be updated

    Returns:
    --------
    Dataframe: updated dataframe with proper data types.
    '''
    
    #clean data
    total_df['cost'] = pd.to_numeric(total_df['price'].apply(lambda x: ''.join(i for i in x if i.isdigit())), errors='coerce')
    total_df['address'] = [x.split(',')[0] for x in total_df['location']]
    total_df['city'] = [x.split(',')[1].strip() for x in total_df['location']]
    total_df['state'] = total_df['location'].apply(lambda x: x.split(',')[-1].split(' ')[-2])
    total_df['zip'] = total_df['location'].apply(lambda x: x.split(',')[-1].split(' ')[-1])
    total_df['beds'] = pd.to_numeric(total_df['details'].apply(lambda x: ''.join(i for i in x[0] if i.isdigit())), errors='coerce')
    total_df['baths'] = pd.to_numeric(total_df['details'].apply(lambda x: ''.join(i for i in x[1] if i.isdigit())), errors='coerce')
    total_df['sq_ft'] = pd.to_numeric(total_df['details'].apply(lambda x: ''.join(i for i in x[2] if i.isdigit())), errors='coerce')
    total_df['time'] = pd.to_datetime(total_df['time'])
    total_df['source'] = 'zillow'

    col= ['details', 'location', 'price']
    total_df.drop(col, axis=1, inplace=True)

    return total_df

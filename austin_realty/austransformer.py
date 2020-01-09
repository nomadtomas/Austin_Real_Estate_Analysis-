import pandas as pd
import numpy as np
import pymongo
from bs4 import BeautifulSoup as bs
#from aus_realty_clean import main


def aus_realty_df(collection):
    '''
    
    '''

    #retrieved data from mongo into a dataframe
    df = pd.DataFrame(list(collection.find()))
    data = df[['html', 'time_scraped']]

    dataframe = []
    for x in data['html']:
        dt = convert_data(x)
        dt['time'] = data['time_scraped']
        dataframe.append(dt)

    complete_df = pd.concat(dataframe)

    complete_df.reset_index(drop=True, inplace=True)
    realty_aus_df = clean_df(complete_df)
    return realty_aus_df

def convert_data(data):
    '''
    Convert html data from realtyaus database into dataframe by obtaining key elements from 
    each webpage.
    
    '''
    
    #initiate beautiful soup html.parser
    soup = bs(data, 'html.parser')
    
    #utilized find_all to obtain elements location
    listings = soup.find_all(class_='articleset listings colset_4')
    mlsids = listings[0].find_all('li', class_="data-mlsid")
    subdivs = listings[0].find_all('li', class_="data-subdivision")
    address = [x.get_text() for x in listings[0].find_all('li', class_="data-address")]
    locs = listings[0].find_all('li', class_="data-location")
    beds = listings[0].find_all('span', class_="details-bedrooms")
    baths = listings[0].find_all('span', class_="details-bathrooms")
    sqfts = listings[0].find_all('span', class_="details-sqft")
    acres = listings[0].find_all('span', class_="details-acres")
    dtypes = listings[0].find_all('li', class_="data-type")
    prices = listings[0].find_all('li', class_="data-price")
    status = listings[0].find_all('li', class_="data-status")
    statusexts = listings[0].find_all('li', class_="data-statusextra")
    photos = listings[0].find_all(class_="photo")
    
    #create lists for each element
    mlsid = [x.get_text(strip=True) for x in mlsids]
    subdiv = [x.get_text(strip=True) for x in subdivs]
    loc = [x.get_text(strip=True) for x in locs]
    bed = [x.get_text(strip=True) for x in beds]
    bath = [x.get_text(strip=True) for x in baths]
    sqft = [x.get_text(strip=True) for x in sqfts]
    acre = [x.get_text(strip=True) for x in acres]
    dtype = [x.get_text(strip=True) for x in dtypes]
    price = [x.get_text(strip=True) for x in prices]
    statu = [x.get_text(strip=True) for x in status]
    statusext = [x.get_text(strip=True) for x in statusexts]
    photo = [x.img['data-src'] for x in photos]
    
    #create a dictionary 
    data = {
        'mlsid': mlsid,
        'subdiv': subdiv,
        'address': address,
        'location': loc,
        'bedrooms': bed,
        'bathrooms': bath, 
        'sqft': sqft,
        'acre': acre,
        'data_type': dtype,
        'price': price,
        'status': statu,
        'status_extra': statusext,
        'photo': photo
    }
    
    #convert dictionary into pandas dataframe, used pd.Series to assure all parameter lengths are equal
    df = pd.DataFrame([pd.Series(value, name=k) for k, value in data.items()]).T
    
    return df

def clean_df(data):
    
    #clean columns 
    data['mls_id'] = data['mlsid'].str.replace(r'\D', '').astype('int')
    data['city'] = data['location'].map(lambda x: x.split(',')[0])
    data['state'] = data['location'].map(lambda x: x.split(',')[1]).str.replace(r'\d', '')
    data['baths'] = data['bathrooms'].str.replace(r'\D', '').astype('float')
    data['sq_ft'] = data['sqft'].str.replace(r'\D', '').astype('float')
    data['acres'] = data['acre'].str.replace(r'AC', '').astype('float')
    data['beds'] = data['bedrooms'].str.replace(r'\D', '').astype('float')
    data['zip'] = data['location'].str.replace(r'\D', '')
    data['cost'] = data['price'].str.replace(r'\D', '').astype('float')
    data['time'] = pd.to_datetime(data['time'])
    data['source'] = 'austin_realty'
    
    #drop unclean columns 
    col = ['mlsid', 'location', 'bathrooms', 'sqft', 'acre', 'bedrooms', 'price']
    data.drop(col, axis=1, inplace=True)
    
    return data

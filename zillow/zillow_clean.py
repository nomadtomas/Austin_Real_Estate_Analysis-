import pandas as pd 
import numpy as np 
import pymongo
from zillowtransformer import zillow_df

def main():
    client = pymongo.MongoClient()
    db = client.zillow
    collection = db.zillow_data
    clean_collection = db.zillow_clean_data

    def transform_data(row):
        data = row.to_dict()
        clean_collection.insert_one(data)

    df = zillow_df(collection)
    clean_df = df.drop_duplicates('listingId')
    clean_df.apply(transform_data, axis=1)

if __name__ == '__main__':
    main()
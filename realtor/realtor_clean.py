import pandas as pd 
import numpy as np 
import pymongo
from realtortransformer import realtor_df

def main():
    client = pymongo.MongoClient()
    db = client.realtor
    collection = db.main_pages
    clean_collection = db.realtor_data

    def transform_data(row):
        data = row.to_dict()
        clean_collection.insert_one(data)   

    df = realtor_df(collection)
    clean_df = df.drop_duplicates('listingId')
    clean_df.apply(transform_data, axis=1)

if __name__ == '__main__':
    main()
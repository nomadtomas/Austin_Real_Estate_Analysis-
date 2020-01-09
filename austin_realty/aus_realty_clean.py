import pandas as pd 
import numpy as np 
import pymongo
from austransformer import aus_realty_df


def main():
    client = pymongo.MongoClient()
    db = client.realtyaus
    collection = db.main_pages
    clean_collection = db.aus_realty_data
   
    def transform_data(row):
        data = row.to_dict()
        clean_collection.insert_one(data)

    df = aus_realty_df(collection)
    df['id'] = df['mls_id'] + df['time']
    clean_df = df.drop_duplicates('mls_id')
    clean_df.apply(transform_data, axis=1)

if __name__ == '__main__':
    main()

import os
import time
import xmlrpc.client
import hashlib
from datetime import datetime

import pandas as pd

from constants import  DAY_FORMAT, INPUT_DATE_FORMAT, SERVING_HOST, SERVING_PORT



def get_hasher():
    # print(url)
    url=f"http://{SERVING_HOST}:{SERVING_PORT}"
    session = xmlrpc.client.ServerProxy(url)    
    return session.handler

def store_names(dataframe):

    names = dataframe["name"].drop_duplicates()

def get_hash(text):
    hash_object = hashlib.sha256(text)
    hex_dig = hash_object.hexdigest()
    return hex_dig

def start_monitoring(args):
    pass
    # for index,tweet in tweets.iterrows():
        
    # hashable

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print (f"{method.__name__} {(te - ts) } seconds") 
        return result
    return timed



def get_day_time(text):
    date_time_obj = datetime.strptime(text, INPUT_DATE_FORMAT)
    return datetime.strftime(date_time_obj,DAY_FORMAT)


def display():
    tweets = pd.read_csv("data/tweets.csv")
    tweets.insert(0,"miss",value=0)
    # for index,tweet in tweets.iterrows():
    #     print(tweets.get(index))
    #     tweets["time"][index] = get_day_time(tweet.time)
    #     print(tweets.get(index))

    tweets["time"] = pd.to_datetime(tweets["time"])

    tegerisch = tweets.groupby(pd.Grouper(key="time",freq="D",)) \
    .apply(lambda gdf: gdf.assign(count=lambda gdf: 1)) \
    # .count()\

    tegerische = tegerisch.groupby(pd.Grouper(key="time",freq="D")).sum() \
    
    print(tegerische)
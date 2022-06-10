
from time import sleep
import pandas as pd
from functions import get_hash, get_hasher, timeit
import matplotlib.pyplot as plt
import time
from numpy import NaN

def test_time():
    tweets = pd.read_csv("data/tweets.csv")
    tweets.insert(0,"time_raw",value=NaN)
    tweets.insert(0,"time_hash",value=NaN)
    # tweets.insert(1,"miss",value=0)
    tweets["time"] = pd.to_datetime(tweets["time"])

    hasher = get_hasher()

    # let the current memory usage be ignored..
    hasher.set_current_memory_usage_as_default()
    # hits = 0
    count = 0
    for index,tweet in tweets.iterrows():
        count+=1
        hex_dig = get_hash(tweet.username.encode('utf-8'))
        # print(f"{hex_dig},{tweet.followers}")
        ts = time.time()
        hasher.add_node_raw(hex_dig,f"{tweet.description},{tweet.location},{tweet.followers},{tweet.numberstatuses}")
        # print(hasher.get_memory_difference())
        tweets.at[index,"time_raw"]=((time.time() - ts) )

    count = 0
    for index,tweet in tweets.iterrows():
        count+=1
        hex_dig = get_hash(tweet.username.encode('utf-8'))
        # print(f"{hex_dig},{tweet.followers}")
        ts = time.time()
        hasher.add_node_hash(hex_dig,f"{tweet.description},{tweet.location},{tweet.followers},{tweet.numberstatuses}")
        tweets.at[index,"time_hash"]=((time.time() - ts) )

    # hasher = get_hasher()
    # print(f"Es ist.. geschaft, der ergebniss ist: {hits},{count},{hits/count}")
    print(f"Total users count: {hasher.get_index_size()}")
    print(f"Memory difference: {hasher.get_memory_difference()}MB")

    return tweets

def run_time_test():
    
    tweets = test_time()
    tegerisch = tweets.groupby(pd.Grouper(key="time",freq="D",)) \
    .apply(lambda gdf: gdf.assign(count=lambda gdf: 1)) \
    # .count()\
    # tegerisch.fillna(method="ffill")
    
    tegerische = tegerisch.groupby(pd.Grouper(key="time",freq="D")).mean() \
    
    print(tegerische)
    
    # tegerische.set_index("time")
    
    df = pd.DataFrame(tegerische,columns=["time","time_raw","time_hash"])
    # df.set_index("time")
    df.plot(y=["time_raw","time_hash"],linestyle="solid",marker="x")
    plt.show()




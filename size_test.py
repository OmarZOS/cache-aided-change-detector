
from numpy import NaN
import pandas as pd
from functions import get_hash, get_hasher, timeit
import matplotlib.pyplot as plt

def run_trace_test():
    
    tweets = test_trace()
    tegerisch = tweets.groupby(pd.Grouper(key="time",freq="D",)) \
    .apply(lambda gdf: gdf.assign(count=lambda gdf: 1)) \
    # .count()\
    print(tegerisch)
    #filling the gaps..
    tegerisch.fillna(method="ffill")
    print(tegerisch)
    tegerische = tegerisch.groupby(pd.Grouper(key="time",freq="D")).mean() \
    
    # print(tegerische)
    # tegerische.set_index("time")
    df = pd.DataFrame(tegerische,columns=["time","memory_raw","memory_hash"])
    # df.set_index("time")
    df.plot(y=["time","trace_raw","trace_hash"],marker="x")
    plt.show()


def test_trace():
    
    tweets = pd.read_csv("data/tweets.csv")
    tweets.insert(0,"memory_raw",value=NaN)
    tweets.insert(0,"memory_hash",value=NaN)
    # tweets.insert(1,"miss",value=0)
    tweets["time"] = pd.to_datetime(tweets["time"])

    hasher = get_hasher()

    # let the current memory usage be ignored..
    hasher.set_current_memory_usage_as_default()
    # hits = 0
    count = 0
    val=0
    for index,tweet in tweets.iterrows():
        count+=1
        hex_dig = get_hash(tweet.username.encode('utf-8'))
        # print(f"{hex_dig},{tweet.followers}")
        hasher.add_node_raw(hex_dig,f"{tweet.description},{tweet.location},{tweet.followers},{tweet.numberstatuses}")
        # print(hasher.get_memory_difference())
        val_update = hasher.get_memory_difference()
        if val_update> val:
            tweets.at[index,"memory_raw"]=val_update
        else:
            tweets.at[index,"memory_raw"]=val

    hasher.set_current_memory_usage_as_default()
    count = 0
    val=0
    for index,tweet in tweets.iterrows():
        count+=1
        hex_dig = get_hash(tweet.username.encode('utf-8'))
        # print(f"{hex_dig},{tweet.followers}")
        hasher.add_node_hash(hex_dig,f"{tweet.description},{tweet.location},{tweet.followers},{tweet.numberstatuses}")
        val_update = hasher.get_memory_difference()
        if val_update> val:
            tweets.at[index,"memory_hash"]=val_update
        else:
            tweets.at[index,"memory_hash"]=val

    # hasher = get_hasher()
    # print(f"Es ist geschaft, der ergebniss ist: {hits},{count},{hits/count}")
    print(f"Total users count: {hasher.get_index_size()}")
    print(f"Memory difference: {hasher.get_memory_difference()}MB")

    return tweets


from time import sleep
import pandas as pd
from functions import get_hash, get_hasher, timeit
import matplotlib.pyplot as plt


@timeit
def insert_nodes():

    tweets = pd.read_csv("data/tweets.csv")
    tweets.insert(0,"miss",value=0)
    # tweets.insert(1,"miss",value=0)
    tweets["time"] = pd.to_datetime(tweets["time"])

    hasher = get_hasher()

    # let the current memory usage be ignored..
    hasher.set_current_memory_usage_as_default()
    # sleep(2000)
    hits = 0
    count = 0

    for index,tweet in tweets.iterrows():
        count+=1
        hex_dig = get_hash(tweet.username.encode('utf-8'))
        # print(f"{hex_dig},{tweet.followers}")
        if(not hasher.add_node_hash(hex_dig,f"{tweet.description},{tweet.location},{tweet.followers},{tweet.numberstatuses}")):
            tweets.at[index,"miss"]=1

    # hasher = get_hasher()
    print(f"Es ist geschaft, der ergebniss ist: {hits},{count},{hits/count}")
    print(f"Total users count: {hasher.get_index_size()}")
    print(f"Memory difference: {hasher.get_memory_difference()}MB")

    return tweets


def run_test():
    
    tweets = insert_nodes()
    tegerisch = tweets.groupby(pd.Grouper(key="time",freq="D",)) \
    .apply(lambda gdf: gdf.assign(count=lambda gdf: 1)) \
    # .count()\

    # tegerisch.fillna(method="ffill")

    tegerische = tegerisch.groupby(pd.Grouper(key="time",freq="D")).sum() \
    
    print(tegerische)


    # tegerische.set_index("time")
    df = pd.DataFrame(tegerische,columns=["time",'count',"miss"])
    df.set_index("time")
    df.plot(y=['count',"miss"])
    plt.show()


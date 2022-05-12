# The perfect dataset for this context is supposed to take users 
# publications into different timestamps timestamps

import pandas as pd
from functions import get_hash, get_hasher, timeit
import matplotlib.pyplot as plt

dates = {}

@timeit
def insert_nodes():

    tweets = pd.read_csv("data/tweets.csv")
    tweets.insert(0,"miss",value=0)
    # tweets.insert(1,"miss",value=0)
    tweets["time"] = pd.to_datetime(tweets["time"])

    hasher = get_hasher()

    # let the current memory usage be ignored..
    hasher.set_current_memory_usage_as_default()

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

def test_memory():
    
    tweets = pd.read_csv("data/tweets.csv")
    tweets.insert(0,"memory_raw",value=0)
    tweets.insert(0,"memory_hash",value=0)
    # tweets.insert(1,"miss",value=0)
    tweets["time"] = pd.to_datetime(tweets["time"])

    hasher = get_hasher()

    # # let the current memory usage be ignored..
    # hasher.set_current_memory_usage_as_default()
    # # hits = 0
    # count = 0
    # for index,tweet in tweets.iterrows():
    #     count+=1
    #     hex_dig = get_hash(tweet.username.encode('utf-8'))
    #     # print(f"{hex_dig},{tweet.followers}")
    #     if(not hasher.add_node_raw(hex_dig,f"{tweet.description},{tweet.location},{tweet.followers},{tweet.numberstatuses}")):
    #         tweets.at[index,"memory_hash"]=hasher.get_memory_difference()

    hasher.set_current_memory_usage_as_default()
    count = 0
    for index,tweet in tweets.iterrows():
        count+=1
        hex_dig = get_hash(tweet.username.encode('utf-8'))
        # print(f"{hex_dig},{tweet.followers}")
        # if(not hasher.add_node_raw(hex_dig,f"{tweet.description},{tweet.location},{tweet.followers},{tweet.numberstatuses}")):
        tweets.at[index,"memory_raw"]=hasher.get_memory_difference()


    # hasher = get_hasher()
    # print(f"Es ist geschaft, der ergebniss ist: {hits},{count},{hits/count}")
    print(f"Total users count: {hasher.get_index_size()}")
    print(f"Memory difference: {hasher.get_memory_difference()}MB")

    return tweets

def run_test():
    
    tweets = insert_nodes()
    tegerisch = tweets.groupby(pd.Grouper(key="time",freq="D",)) \
    .apply(lambda gdf: gdf.assign(count=lambda gdf: 1)) \
    # .count()\

    tegerische = tegerisch.groupby(pd.Grouper(key="time",freq="D")).sum() \
    
    print(tegerische)
    # tegerische.set_index("time")
    df = pd.DataFrame(tegerische,columns=["time",'count',"miss"])
    df.set_index("time")
    df.plot(y=['count',"miss"])
    plt.show()

def run_memory_test():
    
    tweets = test_memory()
    tegerisch = tweets.groupby(pd.Grouper(key="time",freq="D",)) \
    .apply(lambda gdf: gdf.assign(count=lambda gdf: 1)) \
    # .count()\

    tegerische = tegerisch.groupby(pd.Grouper(key="time",freq="D")).sum() \
    
    print(tegerische)
    # tegerische.set_index("time")
    # df = pd.DataFrame(tegerische,columns=["time",'count',"miss"])
    # df.set_index("time")
    # df.plot(y=['count',"miss"])
    # plt.show()



# def FunctionName(args):
    
def master():
    # run_test()
    run_memory_test()


    



if __name__=="__main__":
    master()



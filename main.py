# The perfect dataset for this context is supposed to take users 
# publications into different timestamps timestamps

import pandas as pd
from functions import get_hasher
import hashlib



def tester():

    tweets = pd.read_csv("data/tweets.csv")

    # tweets.sort_values("time")

    hasher = get_hasher()

    hits = 0
    count = 0

    for index,tweet in tweets.iterrows():
        count+=1
        hash_object = hashlib.sha256(tweet.username.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        # print(f"{hex_dig},{tweet.followers}")
        if(hasher.add_node_hash(hex_dig,f"{tweet.followers},{tweet.location},{tweet.followers},{tweet.numberstatuses}")):
            hits+=1

    print(f"Es ist geschaft, der ergebniss ist: {hits},{count},{hits/count}")

# def FunctionName(args):
    


if __name__=="__main__":
        
    hasher = get_hasher()


    tester()

    print(hasher.get_index_size())


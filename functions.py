
import os
import xmlrpc.client


SERVING_HOST = str(os.getenv("HASH_SERVER_HOST"))
SERVING_PORT = int(os.getenv("HASH_SERVER_PORT"))




def get_hasher():
    # print(url)
    url=f"http://{SERVING_HOST}:{SERVING_PORT}"
    session = xmlrpc.client.ServerProxy(url)    
    return session.handler

def store_names(dataframe):

    names = dataframe["name"].drop_duplicates()

def start_monitoring(args):
    pass
    # for index,tweet in tweets.iterrows():
        
    # hashable

import os
import xmlrpc.client

SERVING_HOST = str(os.getenv("HASH_SERVER_HOST"))
SERVING_PORT = int(os.getenv("HASH_SERVER_PORT"))

url=f"http://{SERVING_HOST}:{SERVING_PORT}"
print(url)
proxy = xmlrpc.client.ServerProxy(url)

print(proxy.handler.sumAndDifference(5,6))



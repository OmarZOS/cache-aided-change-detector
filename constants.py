

import os


INPUT_DATE_FORMAT = '%m/%d/%Y %H:%M'
DAY_FORMAT = "%d/%m/%Y"
SERVING_HOST = str(os.getenv("HASH_SERVER_HOST"))
SERVING_PORT = int(os.getenv("HASH_SERVER_PORT"))

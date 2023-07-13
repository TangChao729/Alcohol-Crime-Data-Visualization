import time
from datetime import datetime
import json

import ijson

from backend.Code.Upload.JSONuploader import JSONuploader
import sys
import liquorParser
# append the path of the parent directory
sys.path.append("../..")

with open("liquorConfiguration.json") as f:
    configuration = dict(json.load(f))

# access to local couchDB
address = '172.26.134.184'
port = '5984'
admin = 'admin'
password = 'password'
database_name = 'tweet_data'

# construct js uploader
js_uploader = JSONuploader(address, port, admin, password)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

with open(configuration["file"], "r") as f:
    data = ijson.items(f, 'item')

count = 0
for item in data:
    js_uploader.single_upload(database_name, item)
    count += 1
    if count >= 100: break
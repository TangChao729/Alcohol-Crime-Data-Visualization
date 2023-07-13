import decimal
import time
from datetime import datetime
import json
import ijson
from backend.Code.Upload.JSONuploader import JSONuploader
import sys

with open("twitterConfiguration.json") as f:
    configuration = dict(json.load(f))

# append the path of the parent directory
sys.path.append("../..")

# transfer decimal type into float type
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

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
    data = ijson.items(f,'item')
    count = 0
    for item in data:
        item = json.loads(json.dumps(item, cls=DecimalEncoder))
        js_uploader.single_upload(database_name, item)
        count += 1
        if count >= 100: break
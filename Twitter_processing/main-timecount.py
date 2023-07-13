import json
from datetime import datetime
from collections import Counter


with open("output-vic.json", 'r') as data_file:
    json_data = data_file.read()
data = json.loads(json_data)
tweets = []

for d in data:
    timestamp = d['created_at']
    h = str(datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').hour).zfill(2)
    tweets.append(h)

tweets_count = dict(sorted(Counter(tweets).items()))

with open("output-time-count.json", "w") as file:
    json.dump(tweets_count, file, indent=4)

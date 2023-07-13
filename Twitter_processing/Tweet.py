import json
import re


class Tweet:

    def __init__(self, line):

        json_tweet = json.loads(line)
        self.id = json_tweet["id"] #string
        self.value = json_tweet["value"] # dict
        self.author = json_tweet["doc"]["data"]["author_id"] # string
        self.timestamp = json_tweet["doc"]["data"]["created_at"] # string
        self.language = json_tweet["doc"]["data"]["lang"] # string
        self.like = json_tweet["doc"]["data"]["public_metrics"] # dict
        self.sentiment = json_tweet["doc"]["data"]["sentiment"] # float
        self.geo = json_tweet["doc"]["includes"] if "includes" in json_tweet["doc"] else None # dict

    def create_json(self, tweets):
        processed_tweet = {
            "id": self.id,
            "value": self.value,
            "author_id": self.author,
            "created_at": self.timestamp,
            "lang": self.language,
            "public_metrics": self.like,
            "sentiment": self.sentiment,
            "includes": self.geo
        }
        tweets.append(processed_tweet)


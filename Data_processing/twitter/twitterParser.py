import decimal
import ijson
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

def twitterParser(filename):
    results = []
    with open(filename, 'r', encoding='utf-8') as f:
        # Create an ijson object to iterate over the file
        tweets = ijson.items(f, "rows.item.doc.data")
        for tweet in tweets:
            if type(tweet.get('geo')) is not dict or len(tweet.get('geo')) <= 1: continue
            results.append(tweet)
            if len(results)%10000 == 0: print(len(results))


    with open("twitterWithGeo.json", "w") as f:
        json.dump(results,f, cls=DecimalEncoder)

def twitterTimeParser(filename):
    results = []
    with open(filename, 'r', encoding='utf-8') as f:
        # Create an ijson object to iterate over the file
        times = ijson.items(f, "item.created_at")
        for time in times:
            results.append(int(time[:4]))
    results.sort(key=lambda x:x)
    print(results)
    print(results[0])
    print(results[-1])



if __name__ == '__main__':
    twitterTimeParser(r'D:\COMP90024AS2\data\twitter\twitterWithGeo.json')
    # twitterParser(r"./twitter-huge.json")




import json
from Tweet import Tweet
tweets = []
with open("C:\\Users\swan4\OneDrive\Desktop\\twitter-huge.json", 'r', encoding='utf-8') as file:
    first_line = file.readline()
    print(first_line)
    assert first_line.endswith(",\"rows\":[\n")
    first_line = first_line[:-10] + "}"
    json_first_line = json.loads(first_line)
    print(json_first_line["total_rows"] - json_first_line["offset"])
    i = 0
    j = 0
    while i < 10000:
        line = file.readline()
        tweet = Tweet(line[:-2])
        if tweet.geo:
            tweet.create_json(tweets)
            j += 1
        i += 1
    print(j)
with open("output.json", "w") as file:
    json.dump(tweets, file, indent=4)
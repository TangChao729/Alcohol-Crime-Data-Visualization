import re
import time
from datetime import datetime
import json
import nltk
import JSONuploader
from MastodonCrawler import MastodonCrawler
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
import sys
from nltk.sentiment import SentimentIntensityAnalyzer
# append the path of the parent directory
# nltk.download('punkt')
# nltk.download('vader_lexicon')
sys.path.append("..")


def processMastodon(mastodon_obj):
    # Define the pattern to match the angle brackets and their content
    pattern = r'<[^>]+>'

    key_words = [
        "Alcohol",
        "Beverage",
        "Drink",
        "Booze",
        "Liquor",
        "Beer",
        "Wine",
        "Whiskey",
        "Vodka",
        "Rum",
        "Tequila",
        "Gin",
        "Cocktails",
        "Shots",
        "Champagne",
        "Martini",
        "Margarita",
        "Mojito",
        "Sangria",
        "Cider",
        "Brandy",
        "Sake",
        "Scotch",
        "Bourbon",
        "Liqueur",
        "Absinthe",
        "Aperitif",
        "Digestif",
        "Draught",
        "Stout",
        "Ale",
        "Lager",
        "Pint",
        "Glass",
        "Bottle",
        "Corkscrew",
        "Decanter",
        "Tumbler",
        "Shot glass",
        "Mixer",
        "Ice",
        "Garnish",
        "Strainer",
        "Bar",
        "Pub",
        "Tavern",
        "Brewery",
        "Winery",
        "Distillery",
        "Bartender"
    ]
    stemmer = PorterStemmer()
    stemmed_words = [(word,stemmer.stem(word)) for word in key_words]
    # Use regex to find all occurrences of the pattern and replace them with an empty string
    content = re.sub(pattern, '', mastodon_obj["content"])
    mastodon_obj["tokens"] = {}
    mastodon_obj["sentiment"] = get_sentiment(content)
    if "_id" in mastodon_obj:
        mastodon_obj.pop("_id")
        mastodon_obj.pop("_rev")
    mastodon_obj["sentiment_words"] = get_sentiment_words(content)
    tokens = word_tokenize(content)
    flag = False
    for token in tokens:
        token = stemmer.stem(token)
        for word in stemmed_words:
            if token == word[1]:
                flag = True
                if word[0] in mastodon_obj["tokens"]:
                    mastodon_obj["tokens"][word[0]] += 1
                else:
                    mastodon_obj["tokens"][word[0]] = 1
    return flag

def get_sentiment_words(sentence):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(sentence)
    sentiment_words = []

    for word in sentence.split():
        word_sentiment = sid.polarity_scores(word)
        if word_sentiment['compound'] != 0:
            sentiment_words.append(word)

    return sentiment_words

def get_sentiment(sentence):
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(sentence)

    # Extract compound sentiment score
    compound_score = sentiment_scores['compound']

    return compound_score

# access to mastodon.au with Taylor's token
server_address = 'https://mastodon.au'
# server_token = 'oGi9Wei1yWjj2LGgoRXRJMmKP7gqg0SmWztY7wVwEPc'
# construct crawler
crawler = MastodonCrawler(server_address, "None")

# access to local couchDB
address = '172.26.130.104'
port = '5984'
admin = 'admin'
password = 'your-password'
database_name = 'mastodon_data'

# construct js uploader
js_uploader = JSONuploader.JSONuploader([(address, port, admin, password)])

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

crawler.start_crawling()
# Continuously crawl data
while True:
    # Get data from the generator
    data = next(crawler)
    # data = js_uploader.list_all_docs(database_name)
    if data:
        json_str = json.dumps(data, cls=DateTimeEncoder)
        json_obj = json.loads(json_str)
        if(processMastodon(json_obj)):
            print(json_obj)
            js_uploader.upload(database_name, json_obj)
    else:
        # Add a sleep time to avoid busy waiting
        print("Waiting...")
        # time.sleep(5)


# Stop the crawling after processing a certain amount of data or based on a condition
# crawler.stop_crawling()

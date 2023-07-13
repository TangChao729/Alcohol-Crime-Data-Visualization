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
nltk.download('punkt')
nltk.download('vader_lexicon')
sys.path.append("..")

class SentimentAnalyzer:
    def __init__(self):
        pass

    def processMastodon(self, mastodon_obj):
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
        mastodon_obj["sentiment"] = self.get_sentiment(content)
        if "_id" in mastodon_obj:
            mastodon_obj.pop("_id")
            mastodon_obj.pop("_rev")
        mastodon_obj["sentiment_words"] = self.get_sentiment_words(content)
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

    def get_sentiment_words(self, sentence):
        sid = SentimentIntensityAnalyzer()
        sentiment_scores = sid.polarity_scores(sentence)
        sentiment_words = []

        for word in sentence.split():
            word_sentiment = sid.polarity_scores(word)
            if word_sentiment['compound'] != 0:
                sentiment_words.append(word)

        return sentiment_words

    def get_sentiment(self, sentence):
        sid = SentimentIntensityAnalyzer()
        sentiment_scores = sid.polarity_scores(sentence)

        # Extract compound sentiment score
        compound_score = sentiment_scores['compound']

        return compound_score
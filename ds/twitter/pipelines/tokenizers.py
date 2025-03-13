import re
import pandas as pd
from nltk import download
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

download("stopwords")

stop_words = set(stopwords.words('english'))
tokenizer = TweetTokenizer(reduce_len=True)
stemmer = PorterStemmer()

def tweet_tokenizer(tweet):
    tokens = tokenizer.tokenize(tweet)
    return [stemmer.stem(token) for token in tokens if token not in stop_words]
import re
import pandas as pd
from nltk import download
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

download("stopwords")

stop_words = set(stopwords.words('english'))
tokenizer = TweetTokenizer(reduce_len=True, preserve_case=False, strip_handles=True)
punctuation = '''!”#$%&'()*+,-./:;<=>?@[\]^_`{|}~"’...'''
stemmer = PorterStemmer()

def tweet_tokenizer(tweet):
    tokens = tokenizer.tokenize(tweet)
    tokens = [token for token in tokens if token not in stop_words]
    clear_tokens = []
    for token in tokens:
        if token not in stop_words:
            if token in punctuation:
                continue
            else:
                clear_tokens.append(stemmer.stem(token))
    return clear_tokens

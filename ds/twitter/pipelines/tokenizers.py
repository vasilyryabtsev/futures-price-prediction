import re
import pandas as pd
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)

def clean_tweet(tweet):
    """
    Удаляет ссылки, теги и лишние пробелы из текста твита.
    """
    tweet = re.sub(r"http\S+", "", tweet)  
    tweet = re.sub(r"@\w+", "", tweet)
    tweet = re.sub(r"\s+", " ", tweet).strip()
    return tweet

def tweet_tokenizer(tweet):
    tweet = tweet.lower()
    tokens = tokenizer.tokenize(clean_tweet(tweet))
    return [token for token in tokens if token not in stopwords.words('english')]
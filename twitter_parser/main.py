from twikit import Client, TooManyRequests
import time
from datetime import datetime
import json
from configparser import ConfigParser
from random import randint
import asyncio
import traceback
from tqdm import tqdm
import os
from httpx import ConnectTimeout


DATASET_PATH = 'infl_tweets'
USERNAMES_PATH = 'infl_usernames'
CACHE_PATH = 'infl_cache'
COUNT_FOR_REQUEST = 20
TWEETS_PER_USER = 100
PAUSE_TIME_MIN = 15 * 60
PAUSE_TIME_MAX = 30 * 60
ERORRS = (TooManyRequests, ConnectTimeout)

# login credentials
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']


# Initialize client
client = Client('en-US')


def read_file(path):
    with open(path, mode='r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        return lines

def to_file(path, tweets, username):
    with open(path, mode='a') as file:
        for tweet in tweets:
            new_data = {
                "username": username, # Username
                "name": tweet.user.name, # Author of the tweet.
                "text": tweet.text, # The full text of the tweet.
                "lang": tweet.lang, # The language of the tweet.
                "in_reply_to": tweet.in_reply_to, # The tweet ID this tweet is in reply to, if any
                "is_quote_status": tweet.is_quote_status, # Indicates if the tweet is a quote status.
                # "quote": tweet.quote, # The Tweet being quoted (if any)
                "retweeted_tweet": tweet.retweeted_tweet, # The Tweet being retweeted (if any)
                "possibly_sensitive": tweet.possibly_sensitive, # Indicates if the tweet content may be sensitive.
                "favorited": tweet.favorited, # Indicates if the tweet is favorited.
                "date": tweet.created_at, # The date and time when the tweet was created.
                "quote_count": tweet.quote_count, # The count of quotes for the tweet.
                "reply_count": tweet.reply_count, # The count of replies to the tweet.
                "favorite_count": tweet.favorite_count, # The count of favorites or likes for the tweet.
                "view_count": tweet.view_count, # The count of views.
                "view_count_state": tweet.view_count_state, # The state of the tweet views.
                "retweet_count": tweet.retweet_count, # The count of retweets for the tweet.
                # "place": tweet.place, # The location associated with the tweet.
                "place": None, # The location associated with the tweet.
                "is_translatable": tweet.is_translatable, # Indicates if the tweet is translatable.
                "edits_remaining": tweet.edits_remaining, # The remaining number of edits allowed for the tweet.
                "has_card": tweet.has_card, # Indicates if the tweet contains a card.
                "thumbnail_title": tweet.thumbnail_title, # The title of the webpage displayed inside tweet’s card.
                "urls": tweet.urls, # Information about URLs contained in the tweet.
                "hashtags": tweet.hashtags # Hashtags included in the tweet text.
            }
            json.dump(new_data, file)
            file.write('\n') 

def logout_login(client):
    print('logout')
    client.logout()
    time.sleep(randint(300, 600))
    print('login')
    client.load_cookies('cookies.json')
    
def error_processing(client):
    print(datetime.now())
    print(traceback.format_exc())
    logout_login(client)
    
async def main():
    print('First time logging in? yes/no')
    
    user_answer = input() 
    if user_answer == 'yes':
        await client.login(
            auth_info_1=username ,
            auth_info_2=email,
            password=password
        )
    else:
        client.save_cookies('cookies.json')
    
    client.load_cookies('cookies.json')
    
    usernames = read_file(USERNAMES_PATH)
    
    cache_list = []
    if os.path.exists(CACHE_PATH):
        cache_list = read_file(CACHE_PATH)
    
    
    start_time = time.time()
    pause_time = randint(PAUSE_TIME_MIN, PAUSE_TIME_MAX)
    
    for username in usernames:
        if username in cache_list:
            continue
        if time.time() - start_time > pause_time:
            print('need some time for a break')
            
            client.logout()
            start_time = time.time()
            pause_time = randint(PAUSE_TIME_MIN, PAUSE_TIME_MAX)
            
            print(f'break of {pause_time / 60} min')
            
            time.sleep(pause_time)
            client.load_cookies('cookies.json')
        
        print(f'@{username} processing...')
        query = f'(from:{username})'
        
        try:
            tweets = await client.search_tweet(query, 'Top', count=COUNT_FOR_REQUEST)
            to_file(DATASET_PATH, tweets, username)
        except ERORRS:
            error_processing(client)
            tweets = await client.search_tweet(query, 'Top', count=COUNT_FOR_REQUEST)
            to_file(DATASET_PATH, tweets, username)
        
        for k in tqdm(range(TWEETS_PER_USER // COUNT_FOR_REQUEST - 1)):
            print(f'loaded {(k + 1) * COUNT_FOR_REQUEST} tweets by @{username}')
            time.sleep(randint(5, 15))
            
            try:
                tweets = await tweets.next()
            except ERORRS:
                error_processing(client)
                tweets = await client.search_tweet(query, 'Top', count=COUNT_FOR_REQUEST)
                
            to_file(DATASET_PATH, tweets, username)
            
            if k == TWEETS_PER_USER // COUNT_FOR_REQUEST - 2:
                with open(CACHE_PATH, mode='a') as file:
                    print(username, file=file)
            

asyncio.run(main())
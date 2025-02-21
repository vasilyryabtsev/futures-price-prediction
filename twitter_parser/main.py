import asyncio
import time
from twikit import Client
from itertools import count
from config import QUERY, COUNT
from process_data import save_tweets

client = Client('en-US')

def is_tweets(tweets):
    """
    Проверка на наличие твитов.
    """
    if not tweets:
        print('Tweets not found')
        return False
    return True

async def main():
    client.load_cookies('cookies.json')
    
    tweets = await client.search_tweet(query=QUERY,
                                       product='Latest',
                                       count=COUNT)
    
    counter = count()
    
    while is_tweets(tweets):
        counter = save_tweets(tweets, counter)
        time.sleep(5)
        tweets = await tweets.next()
    
    print(f'Collected {next(counter)} tweets')
    

asyncio.run(main())

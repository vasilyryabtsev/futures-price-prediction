import asyncio
import time
from twikit import Client
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
    
    while is_tweets(tweets):
        time.sleep(5)
        save_tweets(tweets)
        tweets = await tweets.next()

        
asyncio.run(main())
    
    
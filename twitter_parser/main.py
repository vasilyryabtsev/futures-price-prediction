import asyncio
from twikit import Client
from config import QUERY, COUNT

client = Client('en-US')

async def main():
    client.load_cookies('cookies.json')
    
    tweets = await client.search_tweet(query=QUERY,
                                       product='Latest',
                                       count=COUNT)
    
    for tweet in tweets:
        print(tweet.text)
        
asyncio.run(main())
    
    
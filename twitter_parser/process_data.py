import json
import pandas as pd
from config import PATH_JSON, PATH_CSV

def save_tweets(tweets, counter):
    with open(PATH_JSON, mode='a', encoding='utf-8') as file:
        for tweet in tweets:
            new_data = {
                "user_id": tweet.id, # User id
                "text": tweet.text, # The full text of the tweet.
                "lang": tweet.lang, # The language of the tweet.
                "in_reply_to": tweet.in_reply_to, # The tweet ID this tweet is in reply to, if any
                "is_quote_status": tweet.is_quote_status, # Indicates if the tweet is a quote status.
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
                "is_translatable": tweet.is_translatable, # Indicates if the tweet is translatable.
                "edits_remaining": tweet.edits_remaining, # The remaining number of edits allowed for the tweet.
                "has_card": tweet.has_card, # Indicates if the tweet contains a card.
                "thumbnail_title": tweet.thumbnail_title, # The title of the webpage displayed inside tweet’s card.
                "urls": tweet.urls, # Information about URLs contained in the tweet.
                "hashtags": tweet.hashtags # Hashtags included in the tweet text.
            }
            json.dump(new_data, file)
            file.write('\n')
            next(counter)
    return counter
            
if __name__ == "__main__":
    df = pd.read_json(PATH_JSON, lines=True)
    df.to_csv(PATH_CSV, index=False, encoding="utf-8")

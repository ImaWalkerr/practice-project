import datetime
import tweepy
from decouple import config


class TwitterWrapper:
    """
    Tweepy authentication
    """
    def get_tweets_for_game(self, game_name):

        api_key = config('API_KEY', default='')
        api_key_secret = config('API_KEY_SECRET', default='')
        bearer_token = config('BEARER_TOKEN', default='')
        access_token = config('ACCESS_TOKEN', default='')
        access_token_secret = config('ACCESS_TOKEN_SECRET', default='')

        authentication = tweepy.OAuth1UserHandler(api_key, api_key_secret)
        authentication.set_access_token(access_token, access_token_secret)
        api = tweepy.API(authentication)
        """
        Getting tweets for current game
        """
        query_search = game_name
        number_of_tweets = 50
        tweets = []
        authors = []
        time = []

        for item in tweepy.Cursor(api.search_tweets, q=query_search, lang="en", tweet_mode="extended").items(
                number_of_tweets):
            tweets.append(item.full_text)
            authors.append(item.user.screen_name)
            time.append(item.created_at)

        all_data = list(zip(authors, tweets, time))
        return all_data


TWITTER_WRAPPER = TwitterWrapper()

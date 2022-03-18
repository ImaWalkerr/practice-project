import datetime
import requests
from decouple import config


class TwitterWrapper:

    """
    Twitter API wrapper
    """

    API_KEY = config('API_KEY', default='')
    API_SECRET_KEY = config('API_SECRET_KEY', default='')
    ACCESS_TOKEN = config('ACCESS_TOKEN', default='')
    ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET', default='')
    TWITTER_SEARCH_URL = config('TWITTER_SEARCH_URL', default='')

    def __init__(self):
        self.TWITTER_SEARCH_URL = "https://api.twitter.com/1.1/search/tweets.json"

    headers = {
        "Authorization": ACCESS_TOKEN
    }

    def _post(self, params=None):
        return requests.get(self.TWITTER_SEARCH_URL, headers=self.headers, params=params).json()

    def get_tweets_by_game_name(self, game_name, count_of_tweets=3):

        params = {
            "q": "%23{}".format(game_name.replace(" ", "")),
            "tweet_mode": "extended",
            "tweet.fields": "full_text, created_at, user.name",
            "count": count_of_tweets,
        }

        response = self._post(params)
        tweets = response["statuses"]
        tweets = [tweets] if type(tweets) == dict else tweets

        for tweet in tweets:
            tweet["created_at"] = datetime.datetime.strptime(
                tweet["created_at"], "%a %b %d %H:%M:%S %z %Y"
            )

        return tweets

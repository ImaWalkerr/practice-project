import datetime
import requests


# Consumer API keys
# aNI7dhdfTAnK2lF4FX0RKwIWs (API key)
# X99VB3u7Kuyr5kL9angCgM0UTefalqQwWEllkLNElKzMpPfHu1 (API secret key)

# Access token & access token secret
# 180736706-H3H8HrT5QYNE51EVhOHUcEgMaLXZ64xR0pBhvn7Z (Access token)
# LcMy0ekrj2lvXDifJiAagBgevGvbwFs1iQ7FB86ee2lmD (Access token secret)


class TwitterWrapper:

    """
    Twitter API wrapper
    """

    def __init__(self):
        self.twitter_search_url = "https://api.twitter.com/1.1/search/tweets.json"

    headers = {
        "Authorization": "Bearer {180736706-H3H8HrT5QYNE51EVhOHUcEgMaLXZ64xR0pBhvn7Z}"
    }

    def _post(self, params=None):
        return requests.get(self.twitter_search_url, headers=self.headers, params=params).json()

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

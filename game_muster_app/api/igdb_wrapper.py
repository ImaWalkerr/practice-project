import sys
import requests
import json


# Authentication
# Client ID
# t8yrz76lhx8qv5cz7kjpwm61tyni8h


# Client Secret
# 5et0yyr48p4wlsqs26nam8f2mpqm4d


# result = requests.post(
#    'https://id.twitch.tv/oauth2/token?'
#    'client_id=t8yrz76lhx8qv5cz7kjpwm61tyni8h&'
#    'client_secret=5et0yyr48p4wlsqs26nam8f2mpqm4d&'
#    'grant_type=client_credentials')
#
# print(result.text)


# Token
# {"access_token":"yrvss4kvvoggki5m30v6t7uhguybrq","expires_in":4702816,"token_type":"bearer"}

# The base URL is: https://api.igdb.com/v4


class IGDBWrapper:

    headers = {
        "Authorization": "Bearer yrvss4kvvoggki5m30v6t7uhguybrq",
        "Client-ID": "t8yrz76lhx8qv5cz7kjpwm61tyni8h",
    }

    def get_games(self, ids=None):
        where_condition = 'where id=(' + ','.join(map(str, ids)) + ');' if ids else ''

        return requests.post(
            'https://api.igdb.com/v4/games',
            headers=self.headers,
            data='fields id,name,summary,cover.url,genres.name,'
                 'platforms.name,first_release_date,aggregated_rating,aggregated_rating_count,rating,rating_count,'
                 'screenshots.url;' + where_condition).json()

    def get_game(self, game_id):
        return self.get_games(ids=[game_id])

    @staticmethod
    def get_img_path(image_id):
        return "https://images.igdb.com/igdb/" f"image/upload/t_cover_big/{image_id}.jpg"


IGDB_WRAPPER = IGDBWrapper()

import sys
import requests


# Authentication
# Client ID
# t8yrz76lhx8qv5cz7kjpwm61tyni8h

# Client Secret
# 5et0yyr48p4wlsqs26nam8f2mpqm4d


result = requests.post(
    'https://id.twitch.tv/oauth2/token?'
    'client_id=t8yrz76lhx8qv5cz7kjpwm61tyni8h&'
    'client_secret=5et0yyr48p4wlsqs26nam8f2mpqm4d&'
    'grant_type=client_credentials')

print(result.text)


# Token
# {"access_token":"dqwnjlzhfr6stjbb1gyfbqkbwl5r29","expires_in":4702816,"token_type":"bearer"}

# The base URL is: https://api.igdb.com/v4


headers = {
    "Authorization": "Bearer r49ax90ibisv5fweftduanc7qoao11",
    "Client-ID": "t8yrz76lhx8qv5cz7kjpwm61tyni8h",
}

results = requests.post(
    'https://api.igdb.com/v4/games', headers=headers, data='fields age_ratings,aggregated_rating,aggregated_rating_count,alternative_names,artworks,bundles,category,checksum,collection,cover,created_at,dlcs,expanded_games,expansions,external_games,first_release_date,follows,forks,franchise,franchises,game_engines,game_modes,genres,hypes,involved_companies,keywords,multiplayer_modes,name,parent_game,platforms,player_perspectives,ports,rating,rating_count,release_dates,remakes,remasters,screenshots,similar_games,slug,standalone_expansions,status,storyline,summary,tags,themes,total_rating,total_rating_count,updated_at,url,version_parent,version_title,videos,websites;')
with open('test.html', 'w') as output_file:
    output_file.write(results.text)


class IGDBWrapper:
    """
    IGDBWrapper
    """

    def __init__(self, client_id, client_secret):
        self.main_url = 'https://api.igdb.com/v4/'
        self.client_id = client_id
        self.client_secret = client_secret
        self.default_params = {
            "fields": [
                'id',
                'name',
                'summary',
                'cover.image_id',
                'genres.name',
                'platforms.name',
                'created_at.date',
                'first_release_date'
                'aggregated_rating',
                'aggregated_rating_count',
                'rating',
                'rating_count',
                'total_rating',
                'total_rating_count',
                'screenshots.image_id',
            ]
        }

    def get_header(self):
        response = requests.post(
            "https://id.twitch.tv/oauth2/"
            f"token?client_id={self.client_id}"
            f"&client_secret={self.client_secret}"
            "&grant_type=client_credentials"
        )

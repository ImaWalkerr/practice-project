import requests
from decouple import config


class IGDBWrapper:
    """
    Authentication + wrapper
    """
    LOG_URL = config('LOG_URL', default='')
    BASE_URL = config('BASE_URL', default='')
    GAME_URL = config('GAME_URL', default='')
    GENRES_URL = config('GENRES_URL', default='')
    PLATFORMS_URL = config('PLATFORMS_URL', default='')
    CLIENT_ID = config('CLIENT_ID', default='')
    CLIENT_SECRET = config('CLIENT_SECRET', default='')
    BEARER_TOKEN = config('BEARER_TOKEN', default='')

    def get_header(self):
        response = requests.post(
            f"{self.LOG_URL}"
            f"token?client_id={self.CLIENT_ID}"
            f"&client_secret={self.CLIENT_SECRET}"
            "&grant_type=client_credentials"
        )
        if response.status_code == 401:
            raise Exception("Incorrect client id or client secret")

        return {
            "Client-ID": self.CLIENT_ID,
            "Authorization": "Bearer {}".format(response.json()["access_token"]),
        }

    headers = {
        "Authorization": BEARER_TOKEN,
        "Client-ID": CLIENT_ID,
    }

    def get_base_page_games(self):
        return requests.post(
            f"{self.GAME_URL}",
            headers=self.headers,
            data='fields id,'
                 'name,'
                 'cover.url,'
                 'genres.name,'
                 'platforms.name;'
                 'limit 100;'
        ).json()

    def get_games_by_search(self, search=''):
        return requests.post(
            f"{self.GAME_URL}",
            headers=self.headers,
            data='fields id,'
                 'name,'
                 'cover.url,'
                 'genres.name,'
                 'platforms.name;'
                 'limit 100;'
                 + f'search "{search}";' if search else ''
        ).json()

    def get_games_by_filtering(self, platforms='', genres='', ratings=''):
        return requests.post(
            f"{self.GAME_URL}",
            headers=self.headers,
            data='fields id,'
                 'name,'
                 'cover.url,'
                 'genres.name,'
                 'platforms.name;'
                 'limit 100;'
                 + f'where platforms = ["{platforms}"] & genres = ["{genres}"];' if platforms else '' if genres else ''
                 + f'where rating = ("{ratings}");' if ratings else ''
        ).json()

    def get_current_game(self, ids=None):
        where_condition = 'where id=(' + ','.join(map(str, ids)) + ');' if ids else ''
        return requests.post(
            f"{self.GAME_URL}",
            headers=self.headers,
            data='fields id,'
                 'name,'
                 'summary,'
                 'genres.name,'
                 'platforms.name,'
                 'release_dates.human,'
                 'aggregated_rating,'
                 'aggregated_rating_count,'
                 'rating,'
                 'rating_count,'
                 'screenshots.url;'
                 + where_condition
        ).json()

    def get_game_id(self, game_id):
        return self.get_current_game(ids=[game_id])

    def get_genres(self):
        return requests.post(
            f"{self.GENRES_URL}",
            headers=self.headers,
            data='fields name;'
                 'limit 23;'
        ).json()

    def get_platforms(self):
        return requests.post(
            f"{self.PLATFORMS_URL}",
            headers=self.headers,
            data='fields name;'
                 'limit 182;'
        ).json()


IGDB_WRAPPER = IGDBWrapper()

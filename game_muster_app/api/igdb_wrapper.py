import requests
from decouple import config


class IGDBWrapper:

    """
    Authentication + wrapper
    """

    BASE_URL = config('BASE_URL', default='')
    LOG_URL = config('LOG_URL', default='')
    CLIENT_ID = config('CLIENT_ID', default='')
    CLIENT_SECRET = config('CLIENT_SECRET', default='')
    BEARER_TOKEN = config('BEARER_TOKEN', default='')

    def get_header(self):
        response = requests.post(
            "https://id.twitch.tv/oauth2/"
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

    def get_games(self, ids=None):
        where_condition = 'where id=(' + ','.join(map(str, ids)) + ');' if ids else ''

        return requests.post(
            'https://api.igdb.com/v4/games',
            headers=self.headers,
            data='fields id,'
                 'name,'
                 'summary,'
                 'cover.url,'
                 'genres.name,'
                 'platforms.name,'
                 'release_dates.human,'
                 'aggregated_rating,'
                 'aggregated_rating_count,'
                 'rating,'
                 'rating_count,'
                 'total_rating,'
                 'total_rating_count,'
                 'screenshots.url;'
                 'limit 100;'
                 'where (platforms = [6,48] & genres.id = 13) | (platforms = [130,48] & genres = 12);' + where_condition).json()

    def get_game(self, game_id):
        return self.get_games(ids=[game_id])

    def get_genres(self):
        return requests.post(
            'https://api.igdb.com/v4/genres',
            headers=self.headers,
            data='fields name;'
                 'limit 15;'
        ).json()

    def get_platforms(self):
        return requests.post(
            'https://api.igdb.com/v4/platforms',
            headers=self.headers,
            data='fields name;'
                 'limit 15;'
        ).json()

    @staticmethod
    def get_img_path(image_id):
        return "https://images.igdb.com/igdb/" f"image/upload/t_cover_big/{image_id}.jpg"


IGDB_WRAPPER = IGDBWrapper()

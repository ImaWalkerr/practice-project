import requests
from decouple import config


class IGDBWrapper:
    """
    Authentication + wrapper
    """
    LOG_URL = config('LOG_URL_IGDB', default='')
    BASE_URL = config('BASE_URL_IGDB', default='')
    GAME_URL = config('GAME_URL_IGDB', default='')
    GENRES_URL = config('GENRES_URL_IGDB', default='')
    PLATFORMS_URL = config('PLATFORMS_URL_IGDB', default='')
    CLIENT_ID = config('CLIENT_ID_IGDB', default='')
    CLIENT_SECRET = config('CLIENT_SECRET_IGDB', default='')
    BEARER_TOKEN = config('BEARER_TOKEN_IGDB', default='')

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

    PAGE_GAMES_COUNT = 6

    def get_games_count(self, search='', platforms='', genres='', ratings=''):
        data = ('fields id;'
                'limit 500;'
                + (f'where platforms = {platforms};' if platforms else '')
                + (f'where genres = {genres};' if genres else '')
                + (f' & rating >= {ratings[0]} & rating <= {ratings[1]};' if any(ratings) and ratings != (0, 100) else ';')
                + (f'search "{search}";' if search else ''))
        return len(requests.post(
            f"{self.GAME_URL}",
            headers=self.headers,
            data=data
        ).json())

    def get_games_by_filtering(self, search='', platforms='', genres='', ratings='', page=1):
        data = ('fields id,'
                'name,'
                'cover.url,'
                'genres.name,'
                'platforms.name;'
                f'limit {self.PAGE_GAMES_COUNT};'
                f'offset {self.PAGE_GAMES_COUNT * page};'
                + (f'where platforms = {platforms};' if platforms else '')
                + (f'where genres = {genres};' if genres else '')
                + (f' & rating >= {ratings[0]} & rating <= {ratings[1]};' if any(ratings) and ratings != (0, 100) else ';')
                + (f'search "{search}";' if search else ''))
        return requests.post(
            f"{self.GAME_URL}",
            headers=self.headers,
            data=data
        ).json()

    def get_games_for_favorites(self, games_id=''):
        where_condition = 'where id=(' + ','.join(map(str, games_id)) + ');' if games_id else ''
        data = ('fields name,'
                'cover.url,'
                'genres.name;'
                'limit 500;'
                + where_condition)
        return requests.post(
            f"{self.GAME_URL}",
            headers=self.headers,
            data=data
        ).json()

    @staticmethod
    def get_img_path(img_id):
        return "https://images.igdb.com/igdb/" f"image/upload/t_cover_big/{img_id}.jpg"

    def get_games_for_manager(self):
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
                 'cover.url,'
                 'screenshots.url;'
                 'limit 500;'
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
                 'cover.url,'
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
                 'limit 500;'
        ).json()

    def get_platforms(self):
        return requests.post(
            f"{self.PLATFORMS_URL}",
            headers=self.headers,
            data='fields name;'
                 'limit 500;'
        ).json()


IGDB_WRAPPER = IGDBWrapper()

from game_muster_app.models import *
from game_muster_app.api.igdb_wrapper import IGDB_WRAPPER


class BaseGameManager:
    """
    Base game manager
    """
    def create_game_from_igdb(self):
        games_from_igdb = IGDB_WRAPPER.get_games_for_manager()
        stored_games = Games.objects.filter(game_id=games_from_igdb['id']).first()

        if stored_games:
            return stored_games

        games = Games.objects.create(
            game_id=games_from_igdb.get('id'),
            game_name=games_from_igdb.get('name'),
            release_dates=games_from_igdb.get('release_dates'),
            cover_url=games_from_igdb.get('cover'),
            game_summary=games_from_igdb.get('summary'),
            rating=games_from_igdb.get('rating'),
            rating_count=games_from_igdb.get('rating_count'),
            aggregated_rating=games_from_igdb.get('aggregated_rating'),
            aggregated_rating_count=games_from_igdb.get('aggregated_rating_count'),
        )

        for platform in games_from_igdb['platforms'] or []:
            games.platforms.add(Platforms.objects.get_or_create(platform_name=platform)[0])

        for genre in games_from_igdb['genres'] or []:
            games.genres.add(Genres.objects.get_or_create(genre_name=genre)[0])

        for screenshot in games_from_igdb['screenshots'] or []:
            ScreenShots.objects.create(game=games, screenshot_url=screenshot)

        return games


class GamesManager(BaseGameManager):
    """
    IGDB API games manager
    """
    def generate_list_of_games(self):
        games = []
        game = self.create_game_from_igdb()
        games.append(game)
        return games

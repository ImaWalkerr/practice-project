from game_muster_app.models import *
from game_muster_app.api.igdb_wrapper import IGDB_WRAPPER


class GameManager:
    """
    Base game manager script
    """
    def create_game_from_igdb(self):
        offset = 0
        while True:
            games_from_igdb = IGDB_WRAPPER.get_games_for_manager(offset)
            offset += 500
            if games_from_igdb is []:
                break
            for value in games_from_igdb:
                stored_games = Games.objects.filter(game_id=value.get('id')).first()
                if stored_games:
                    update_games = Games.objects.filter(game_id=value.get('id')).update(
                        game_name=value.get('name'),
                        game_summary=value.get('summary') if value.get('summary') else None,
                        release_dates=value.get('release_dates')[0].get('human')
                        if value.get('release_dates') and len(value.get('release_dates')) else None,
                        cover_url=value.get('cover').get('url').replace('t_thumb', 't_cover_big')
                        if value.get('cover') else None,
                        rating=value.get('rating') if value.get('rating') else 0,
                        rating_count=value.get('rating_count') if value.get('rating_count') else 0,
                        aggregated_rating=value.get('aggregated_rating') if value.get('aggregated_rating') else 0,
                        aggregated_rating_count=value.get('aggregated_rating_count')
                        if value.get('aggregated_rating_count') else 0,
                    )
                    print(f"Successfully game '{stored_games}' updated")

                else:
                    new_games = Games.objects.create(
                        game_id=value.get('id'),
                        game_name=value.get('name'),
                        game_summary=value.get('summary') if value.get('summary') else None,
                        release_dates=value.get('release_dates')[0].get('human')
                        if value.get('release_dates') and len(value.get('release_dates')) else None,
                        cover_url=value.get('cover').get('url').replace('t_thumb', 't_cover_big')
                        if value.get('cover') else None,
                        rating=value.get('rating') if value.get('rating') else 0,
                        rating_count=value.get('rating_count') if value.get('rating_count') else 0,
                        aggregated_rating=value.get('aggregated_rating') if value.get('aggregated_rating') else 0,
                        aggregated_rating_count=value.get('aggregated_rating_count')
                        if value.get('aggregated_rating_count') else 0,
                    )

                    if 'platforms' in value:
                        for platform in value['platforms']:
                            new_games.game_platforms.add(
                                Platforms.objects.get_or_create(platform_id=platform.get('id'),
                                                                platform_name=platform.get('name'))[0]
                            )

                    if 'genres' in value:
                        for genre in value['genres']:
                            new_games.game_genres.add(
                                Genres.objects.get_or_create(genre_id=genre.get('id'), genre_name=genre.get('name'))[0]
                            )

                    if 'screenshots' in value:
                        for screenshot in value['screenshots']:
                            ScreenShots.objects.update_or_create(
                                game=new_games,
                                screenshot_url=screenshot.get('url').replace('t_thumb', 't_screenshot_huge')
                            )
                    print(f"Successfully game '{new_games}' created")

        return "Successfully games loaded"


GAME_MANAGER = GameManager()

from django.core.management.base import BaseCommand, CommandError
from game_muster_app.managers.base_game_manager import GamesManager
from game_muster_app.models import Games


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            latest_game = (
                Games.objects.exclude(release_dates=None).order_by('-release_dates').first()
            )
            last_release_date = latest_game.release_dates if latest_game else None

            GamesManager.generate_list_of_games(last_release_date)
        except Games.DoesNotExist:
            raise CommandError('Games does not exist')

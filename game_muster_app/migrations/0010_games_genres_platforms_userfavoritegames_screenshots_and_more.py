# Generated by Django 4.0.2 on 2022-04-01 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('game_muster_app', '0009_delete_userfavoritegames'),
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.IntegerField(default=0, verbose_name='Game Id from Igdb.com')),
                ('game_name', models.CharField(max_length=124, verbose_name='Game name')),
                ('game_summary', models.TextField(max_length=1024, verbose_name='Game summary')),
                ('cover_url', models.CharField(max_length=256, verbose_name='Game cover')),
                ('release_dates', models.DateTimeField(default=None, null=True, verbose_name='Game release dates')),
                ('rating', models.DecimalField(decimal_places=2, default=None, max_digits=4, null=True, verbose_name='Game rating')),
                ('rating_count', models.IntegerField(default=None, null=True, verbose_name='Game rating count')),
                ('aggregated_rating', models.DecimalField(decimal_places=2, default=None, max_digits=4, null=True, verbose_name='Game aggregated rating')),
                ('aggregated_rating_count', models.IntegerField(default=None, null=True, verbose_name='Game aggregated rating count')),
            ],
            options={
                'verbose_name': 'Games catalog',
                'verbose_name_plural': 'Games catalogs',
                'db_table': 'games',
            },
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_id', models.IntegerField(default=0, verbose_name='Genre id')),
                ('genre_name', models.CharField(max_length=124, verbose_name='Genre name')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
                'db_table': 'genres',
            },
        ),
        migrations.CreateModel(
            name='Platforms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform_id', models.IntegerField(default=0, verbose_name='Platform id')),
                ('platform_name', models.CharField(max_length=124, verbose_name='Platform name')),
            ],
            options={
                'verbose_name': 'Platform',
                'verbose_name_plural': 'Platforms',
                'db_table': 'platforms',
            },
        ),
        migrations.CreateModel(
            name='UserFavoriteGames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorite_games', to='game_muster_app.games', verbose_name='User games')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_favorites', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'User wishlist',
                'verbose_name_plural': 'Users wishlists',
                'db_table': 'user_wishlist',
            },
        ),
        migrations.CreateModel(
            name='ScreenShots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenshot_url', models.CharField(max_length=256, verbose_name='Game screenshot')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_screenshots', to='game_muster_app.games', verbose_name='Game')),
            ],
            options={
                'verbose_name': 'Screenshot',
                'verbose_name_plural': 'Screenshots',
                'db_table': 'screenshots',
            },
        ),
        migrations.AddField(
            model_name='games',
            name='favorite_games',
            field=models.ManyToManyField(related_name='game_in_users_favorites', through='game_muster_app.UserFavoriteGames', to=settings.AUTH_USER_MODEL, verbose_name='game_in_users_favorites'),
        ),
        migrations.AddField(
            model_name='games',
            name='game_genres',
            field=models.ManyToManyField(related_name='game_genres', to='game_muster_app.Genres', verbose_name='Game genres'),
        ),
        migrations.AddField(
            model_name='games',
            name='game_platforms',
            field=models.ManyToManyField(related_name='game_platforms', to='game_muster_app.Platforms', verbose_name='Game platforms'),
        ),
    ]
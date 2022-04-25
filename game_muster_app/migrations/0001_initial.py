# Generated by Django 4.0.2 on 2022-04-22 09:15

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('birthday', models.DateField(default=0, verbose_name='Birthday')),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], default='MALE', max_length=6, verbose_name='Gender')),
                ('email_verify', models.BooleanField(default=False, verbose_name='Email verification status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.IntegerField(default=0, unique=True, verbose_name='Game Id from Igdb.com')),
                ('game_name', models.CharField(max_length=124, verbose_name='Game name')),
                ('game_summary', models.TextField(max_length=1024, null=True, verbose_name='Game summary')),
                ('cover_url', models.CharField(max_length=256, null=True, verbose_name='Game cover')),
                ('release_dates', models.CharField(max_length=124, null=True, verbose_name='Game release dates')),
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
                ('screenshot_url', models.CharField(max_length=256, null=True, verbose_name='Game screenshot')),
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

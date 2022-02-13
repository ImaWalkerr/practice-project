# Generated by Django 3.2.6 on 2022-02-11 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_muster_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScreenShots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info_image', models.CharField(max_length=255, verbose_name='Описание')),
                ('screenshots', models.ImageField(upload_to='media/screenshots', verbose_name='Скриншоты')),
            ],
            options={
                'verbose_name': 'Скриншот',
                'verbose_name_plural': 'Скриншоты',
            },
        ),
        migrations.RenameField(
            model_name='games',
            old_name='game_info',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='games',
            name='genre',
        ),
        migrations.AddField(
            model_name='games',
            name='genres',
            field=models.CharField(choices=[('arcade', 'Аркада'), ('action', 'Экшн'), ('strategy', 'Стратегия'), ('sport', 'Спорт'), ('adventure', 'Приключения'), ('rpg', 'Ролевые')], default='arcade', max_length=255, verbose_name='Жанр'),
        ),
        migrations.AddField(
            model_name='games',
            name='platforms',
            field=models.CharField(default=1, max_length=255, verbose_name='Платформы'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='games',
            name='release_date',
            field=models.CharField(default=1, max_length=255, verbose_name='Дата выхода'),
            preserve_default=False,
        ),
    ]
# Generated by Django 4.0.2 on 2022-02-27 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_muster_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title1', models.TextField(max_length=24, verbose_name='title_1')),
                ('title2', models.TextField(max_length=24, verbose_name='title_2')),
                ('title3', models.TextField(max_length=24, verbose_name='title_3')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
            },
        ),
    ]

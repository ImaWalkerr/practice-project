# Generated by Django 4.0.2 on 2022-03-14 14:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game_muster_app', '0004_alter_gameuser_birthday_alter_gameuser_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameuser', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]

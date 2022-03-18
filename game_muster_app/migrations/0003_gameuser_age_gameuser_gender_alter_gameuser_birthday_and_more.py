# Generated by Django 4.0.2 on 2022-03-09 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game_muster_app', '0002_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameuser',
            name='age',
            field=models.IntegerField(default=0, verbose_name='Age'),
        ),
        migrations.AddField(
            model_name='gameuser',
            name='gender',
            field=models.CharField(default=1, max_length=124, verbose_name='Gender'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='birthday',
            field=models.DateField(verbose_name='Birthday'),
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
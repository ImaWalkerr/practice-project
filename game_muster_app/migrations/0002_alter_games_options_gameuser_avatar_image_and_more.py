# Generated by Django 4.0.2 on 2022-04-29 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_muster_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='games',
            options={'ordering': ['id'], 'verbose_name': 'Games catalog', 'verbose_name_plural': 'Games catalogs'},
        ),
        migrations.AddField(
            model_name='gameuser',
            name='avatar_image',
            field=models.ImageField(default=1, upload_to='static/media/avatars', verbose_name='user_avatar_image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gameuser',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=6, verbose_name='Gender'),
        ),
    ]
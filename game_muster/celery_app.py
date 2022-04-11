from __future__ import absolute_import, unicode_literals
"""
Celery config file

https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html

"""
import os
from celery import Celery
from celery.schedules import crontab

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_muster.settings')

# you change the name here
app = Celery('game_muster')

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# load tasks.py in django apps
app.conf.beat_schedule = {
    'add_new_games': {
        'task': 'game_muster_app.tasks.refresh_games',
        'schedule': crontab(hour='*/12'),
    }
}

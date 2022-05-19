                                           GameMuster
                                           
What is it?
-----------

This is iTechArt internship task.
The main goal is to improve develop skills.

OverView
------------------

This website is created for gamers who love playing games and always looking 
for something new to play.

You can look for new games by simple search by game name or 
using filters (platforms, genres and ratings). 

Also after registration you as user can add games to you wish list (MUST's).
It will help you a lot to save all your games if you want to play them soon or 
come back to the game later.

Project stack:
-------------

- [x] Python 3.9.8
- [x] Django 4.0.2
- [x] DRF Rest api
- [x] HTML5 (BEM methodology)
- [x] CSS (Scss, Sass) using FileWatchers
- [x] Javascript (ES2015+)
- [x] Celery 5.2.6 for tasks
- [x] Celery-beat 2.2.1 for schedule tasks
- [x] PostgreSQL 11
- [x] Docker, docker-compose

<div>
    <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg"  title="Python" alt="Python" width="40" height="40"/>&nbsp;
    <img src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain-wordmark.svg"  title="Django" alt="Django" width="40" height="40"/>&nbsp;
    <img src="https://github.com/devicons/devicon/blob/master/icons/javascript/javascript-original.svg" title="JavaScript" alt="JavaScript" width="40" height="40"/>&nbsp;
    <img src="https://github.com/devicons/devicon/blob/master/icons/css3/css3-plain-wordmark.svg"  title="CSS3" alt="CSS" width="40" height="40"/>&nbsp;
    <img src="https://github.com/devicons/devicon/blob/master/icons/html5/html5-original.svg" title="HTML5" alt="HTML" width="40" height="40"/>&nbsp;
    <img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original-wordmark.svg"  title="Postgresql" alt="Postgresql" width="40" height="40"/>&nbsp;
</div>

Games were taken from:

- [x] [Twitch](https://www.igdb.com/api) IGDB API
- [x] [Twitter](https://developer.twitter.com/en/docs) API

Also:

For deploy using:
- [x] unicorn
- [x] nginx
- [x] [Heroku](https://www.heroku.com/)

How to run website with Docker:
-------------

### For Windows

##### Check Requirements for Hyper-V
Windows 10 Enterprise, Pro, or Education
64-bit Processor with Second Level Address Translation (SLAT).
CPU support for VM Monitor Mode Extension (VT-c on Intel CPUs).
Minimum of 4 GB memory.
The Hyper-V role cannot be installed on Windows 10 Home.

##### Check Requirements for WSL-2
Windows 10 version 2004 or higher (build 19041 or higher) or Windows 11.

- You need to activate [Hyper-V](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v) 
and then install and activate [WSL-2](https://docs.microsoft.com/ru-ru/windows/wsl/install)
- You need to install [Docker](https://www.docker.com/products/docker-desktop/) (put mark use `WSL-2 configuration`)
or you can use plugin in your [IDE](https://blog.jetbrains.com/pycharm/2017/08/using-docker-compose-on-windows-in-pycharm/) (PyCharm for example)
- where you need to choose .exe file.

For Windows in Dockerfile:
change line - `RUN pip install -r requirements.txt`
to line - `RUN pip install -r requirements_windows.txt`

- In the `Terminal` use command to create and start containers:
```sh
docker-compose build
```
if you want to make changes in docker-compose and accept them use command:
```sh
docker-compose up
```

### For Linux OS

- You need to install [Docker](https://www.docker.com/products/docker-desktop/)
or you can use plugin in your IDE - where you need to choose docker file.

- In the `Terminal` use command to create and start containers:
```sh
sudo docker-compose build
```
if you want to make changes in docker-compose and accept them use command:
```sh
sudo docker–compose up
```

How to run website local:
-------------

`Warning!`
**If you use** `Windows 10 PRO` >>>
Install dependencies from the requirements_windows.txt:
```sh
pip install requirements_windows.txt
```
`Warning!`
**If you use** `Linux OS` >>>
Install dependencies from the requirements.txt:
```sh
pip install -r requirements.txt
```

After cloning repository and downloading dependencies 
you need to set environmental variables connected to:

[PostgreSQL](https://docs.djangoproject.com/en/3.2/ref/settings/#databases) 
(`PostgreSQL` **is the default here):**
- DATABASE_ENGINE
- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD
- DATABASE_HOST
- DATABASE_PORT

[Email confirmation](https://docs.djangoproject.com/en/3.2/topics/email/#send-mail):
- EMAIL_BACKEND
- EMAIL_HOST 
- EMAIL_PORT 
- EMAIL_USE_TLS
- EMAIL_HOST_USER 
- EMAIL_HOST_PASSWORD

**If you want** to get email confirmation email local >>>
put this line in your `settings.py`

- EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


[Twitch](https://www.igdb.com/api) IGDB API:

- IGDB_CLIENT_ID
- IGDB_CLIENT_SECRET

[Twitter](https://developer.twitter.com/en/docs) API

- TWITTER_BEARER_TOKEN

Now you're ready to run the `server`:

You can use **Edit configuration** for your `manage.py` and 
put `runserver` in parameters and apply changes.
After that you can start server just click on `green arrow` and you good to go!

Also:
- For `Windows 10 PRO` use:

```sh
python manage.py runserver
```

- For `Linux OS` use:

```sh
export YOUR_VAR=<value>
...
python manage.py runserver
```

# Finhub project

## Major steps to install django with postgres and to run it in container
* Create folder `django` and in it: `Dockerfile` and `requirements.txt` files
* In main folder create docker-compose.yaml file
* In main folder execute `docker-compose run --rm dj bash` to run the containers and enter in bash
* Execute `django-admin startproject project .` and `python manage.py startapp finhub` to create the project and the application
* Edit `settings.py` in `django\project` folder by replacing 

>DATABASES = {
>    'default': {
>        'ENGINE': 'django.db.backends.postgresql',
>        'NAME': 'postgres',
>        'USER': 'postgres',
>        'PASSWORD': 'postgres',
>        'HOST': 'db',
>        'PORT': 5432,
>    }
>}
>
>and by adding `'finhub',` in `INSTALLED_APPS =`
>
>and by replacing `ALLOWED_HOSTS = ['*']`
>

* Run it with `docker-compose up -V -d --build` or `docker-compose up`

* Test it at http://localhost/

## Finhub landing page & superuser
* Edit `urls.py` and `settings.py` in `project`
* Create `static` folder
* Edit `views.py` in `finhub`
* Create `urls.py` in `finhub`
* Create `docker-entrypoint.sh`, `gconfig.py` and `.env` files in `django` folder
* Edit `Dockerfile`
* Start with `docker-compose up -V --build` and visit `http://localhost/finhub/`
* Stop with Ctr + C




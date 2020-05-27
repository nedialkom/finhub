# finhub project

## Major steps
1. Create folder `django` and in it: `Dockerfile` and `requirements.txt` files
2. In main folder create docker-compose.yaml file
3. In main folder execute `docker-compose run --rm dj bash` to run the containers and enter in bash
4. Execute `django-admin startproject project .` and `python manage.py startapp finhub` to create the project and the application
5. Edit `settings.py` in `django\project` folder by replacing 

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

6. Run it with `docker-compose up -V -d --build` or `docker-compose up`

7. Test it at http://localhost/




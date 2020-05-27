#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput --dry-run

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

echo "Creating superuser"
script="
from django.contrib.auth.models import User;

username = '$DJANGO_SUPERUSER_USERNAME';
password = '$DJANGO_SUPERUSER_PASSWORD';
email = '$DJANGO_SUPERUSER_EMAIL';

if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped.');
"
printf "$script" | python manage.py shell

# Start server
# Development with python, production with gunicorn
echo "Starting server"
python manage.py runserver 0.0.0.0:80
#exec gunicorn -c gconfig.py --log-file=- project.wsgi:application
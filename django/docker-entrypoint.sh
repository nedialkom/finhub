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

echo "Starting Elasticsearch indexing ..."
script2="
import elasticsearch
import time
es = elasticsearch.Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
while True:
    try:
        es.search(index='')
        break
    except (
        elasticsearch.exceptions.ConnectionError,
        elasticsearch.exceptions.TransportError
    ):
        time.sleep(1)
"

printf "$script2" | python manage.py shell

set -o errexit
#set -o pipefail
set -o nounset

#index data from the relational database into Elasticsearch
python manage.py search_index --rebuild -f

# Start server
# Development with python, production with gunicorn
echo "Starting server"
python manage.py runserver 0.0.0.0:80
#exec gunicorn -c gconfig.py --log-file=- project.wsgi:application
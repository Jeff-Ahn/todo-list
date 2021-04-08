#!/bin/bash

maridb_host="mariadb"
maridb_port=3306

# Wait for the postgres docker to be running
while ! nc $maridb_host $maridb_port; do
  >&2 echo "MariaDB is unavailable - sleeping"
  sleep 5
done

echo "Run collectstatic"
python manage.py collectstatic --no-input
echo "Run makemigrations"
python manage.py makemigrations
echo "Run migrate"
python manage.py migrate

gunicorn backend.wsgi:application --bind 0.0.0.0:8000
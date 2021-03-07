#!/bin/bash

maridb_host="mariadb"
maridb_port=3306

# Wait for the postgres docker to be running
while ! nc $maridb_host $maridb_port; do
  >&2 echo "MariaDB is unavailable - sleeping"
  sleep 1
done

CONTAINER_ALREADY_STARTED="CONTAINER_ALREADY_STARTED_PLACEHOLDER"

if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    touch $CONTAINER_ALREADY_STARTED
    echo "-- First container startup --"
    echo "Rum makemigrations 'account' App"
    python manage.py makemigrations account
    python manage.py collectstatic
else
    echo "-- Not first container startup --"
fi

echo "Run migrate"
python manage.py migrate

gunicorn todo.wsgi:application --bind 0.0.0.0:8000
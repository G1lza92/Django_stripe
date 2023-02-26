#!/bin/bash

echo "Make migrations database"
python manage.py migrate

echo "Apply database migrations"
python manage.py migrate

exec "$@"
#!/bin/sh
set -e

cd src/
python manage.py migrate --noinput
python manage.py add_locations
python manage.py add_cars
python manage.py runserver 0.0.0.0:8000 --noreload

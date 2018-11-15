#!/bin/bash
set -e
envsubst < /uwsgi.ini.template > /uwsgi.ini
echo "Setting up project"
python manage.py collectstatic --noinput
python manage.py migrate
echo "Running Command $@"
exec "$@"

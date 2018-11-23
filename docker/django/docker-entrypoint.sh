#!/bin/bash
set -e
envsubst < /uwsgi.ini.template > /uwsgi.ini
echo "Setting up project"
python36 manage.py collectstatic --noinput
python36 manage.py migrate
echo "Running Command $@"
exec "$@"

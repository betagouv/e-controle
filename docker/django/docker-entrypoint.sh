#!/bin/bash
set -e

printf "\n\nCollect static files"
python manage.py collectstatic --noinput

printf "\n\nApply database migrations"
python manage.py migrate

printf "\n\nIP address:\n"

hostname -i

printf "\n\n"

exec "$@"

#!/bin/bash
set -e
if [ -f ".env" ] ; then echo "Loading .env file..." ; source .env ; fi
echo "Setting up project"
python3.6 manage.py collectstatic --noinput
python3.6 manage.py migrate
echo "Running Command $@"
exec "$@"

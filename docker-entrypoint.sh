#!/bin/bash
set -e
echo "Setting up project"
python3.6 manage.py collectstatic --noinput
python3.6 manage.py migrate
echo "Running Command $@"
exec "$@"

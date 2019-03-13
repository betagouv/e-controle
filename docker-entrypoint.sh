#!/bin/bash
set -e

if [ -f ".env" ] ;
then
    echo "############# Loading .env file..." ;
    source .env ;
fi

echo "############# Running Django collectstatic and migrate"""
python3.6 manage.py collectstatic --noinput
python3.6 manage.py migrate

echo -n "############# Server IP: "
hostname -I

echo "############# Server Port: $PORT"

case "$1" in
    dev)
        echo "############# Running Development Server on ${PORT}"
        python3.6 manage.py runserver 0:${PORT}
    ;;
    uwsgi)
        echo "############# Running uWSGI App"
        uwsgi --ini uwsgi.ini
    ;;
    *)
        echo "############# Running Command: $@"
        exec "$@"
    ;;
esac

#!/bin/bash
set -e

if [ -f ".env" ] ;
then
    echo "############# Loading .env file..." ;
    source .env ;
fi

initialize_app()
{
    echo "############# Running Django collectstatic and migrate"""
    pip3 install -r requirements.txt
    python3.6 manage.py migrate
    python3.6 manage.py collectstatic --noinput

    echo "############# Building bundle"""
    npm run build-all
}

echo -n "############# Server IP: "
hostname -I

echo "############# Server Port: $PORT"

case "$1" in
    dev)
        initialize_app
        echo "############# Running Development Server on ${PORT}"
        python3.6 manage.py runserver 0:${PORT}
    ;;
    sh)
        initialize_app
        bash
    ;;
    uwsgi)
        initialize_app
        echo "############# Running uWSGI App"
        uwsgi --ini uwsgi.ini
    ;;
    *)
        echo "############# Running Command: $@"
        exec "$@"
    ;;
esac

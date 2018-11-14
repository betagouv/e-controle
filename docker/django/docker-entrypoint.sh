#!/bin/bash
set -e

case "$1" in
    setup)
        echo "Setting up project"
        python manage.py collectstatic --noinput
        python manage.py migrate
    ;;
    dev)
        echo "Running Development Server on 0.0.0.0:${PORT}"
        python manage.py runserver 0.0.0.0:${PORT}
    ;;
    bash)
        /bin/bash "${@:2}"
    ;;
    manage)
        python manage.py "${@:2}"
    ;;
    python)
        python "${@:2}"
    ;;
    shell)
        python manage.py shell_plus
    ;;
    uwsgi)
        echo "Running uWSGI..."
        uwsgi --ini /uwsgi.ini
    ;;
    *)
        echo "Running Command $@"
        exec "$@"
    ;;
esac

#!/bin/sh

PROJECT_DIR=/opt/e-controle/
VENV_DIR=/opt/venv/
CONF_DIR=/opt/conf

# Set environnement
source $PROJECT_DIR/.env

# We need a proxy to acces the web
export {http,https,ftp}_proxy=$PROXY

# Django deployment

source $VENV_DIR/bin/activate

cd $PROJECT_DIR
git pull
pip install -r requirements.txt
./manage.py migrate
./manage.py collectstatic --noinput

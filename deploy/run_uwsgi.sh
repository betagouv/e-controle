#!/bin/sh
PROJECT_DIR=/opt/e-controle/
cd $PROJECT_DIR
source .env
uwsgi uwsgi.ini

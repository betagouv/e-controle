#!/bin/sh

yum -y install redis
systemctl start redis
systemctl enable redis
redis-cli ping

celery worker --beat -A ecc -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &> /var/log/ecc-celery-beat.log &

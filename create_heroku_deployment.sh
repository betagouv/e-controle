#!/usr/bin/env bash

# Checkout the git branch you want to use, then run this script.

# create a heroku instance
heroku apps:create my-instance-name
git remote add heroku git@heroku.com:my-instance-name.git # if you already have a heroku remote, you'll need to delete it
git push heroku master # you have to push to master, the other branches are ignored on heroku

# add postgres to your instance
heroku addons:create heroku-postgresql:hobby-dev
# Outputs something like : Created postgresql-elliptical-45023 as DATABASE_URL

# Save the postgres url
DB_URL="$(heroku pg:credentials:url DATABASE_URL | grep 'postgres://')"

# upload db dump from git repo. THIS DESTROYS THE CURRENT DB! (if there is one)
heroku pg:backups:restore 'https://raw.githubusercontent.com/betagouv/e-controle/develop/db.dump' DATABASE_URL


# set config vars
heroku config:set DEBUG=True
heroku config:set SECRET_KEY=bWqXNig8i3EQwlT-t6OlNU7U_4bk5jJISw7fkB6EkCBOmT7uqatcBw8H

heroku config:set DEFAULT_FROM_EMAIL=e-controle@beta.gouv.fr
heroku config:set EMAIL_HOST=debugmail.io
heroku config:set EMAIL_HOST_PASSWORD=9a62db60-fa14-11e8-a724-49f5a38ee8ee
heroku config:set EMAIL_HOST_USER=estelle.comment@gmail.com
heroku config:set EMAIL_PORT=25

heroku config:set DATABASE_URL=${DB_URL}
heroku config:set STAGING_DATABASE_URL=postgres://ijrphgdxjsfyyl:6311267c9240ee54d933f745d4343724eddea476b2be271c6d93477987a1ee3c@ec2-79-125-124-30.eu-west-1.compute.amazonaws.com:5432/d150jki8bk56cd

heroku config:set CELERY_BROKER_URL=ignore

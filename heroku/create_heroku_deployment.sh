#!/usr/bin/env bash

# First download the heroku cli : https://devcenter.heroku.com/articles/heroku-cli#download-and-install
# Edit the vars where needed.

# You will get my-instance-name.herokuapp.com
INSTANCE_NAME='<your instance name>'

# create a heroku instance
heroku apps:create ${INSTANCE_NAME}

# add postgres to your instance
heroku addons:create --app ${INSTANCE_NAME} heroku-postgresql:hobby-dev

# Get url for db dump, from e-controle-openlab.herokuapp.com
DUMP_URL="$(heroku pg:backups:url b006 --app e-controle-openlab)"
# Upload db dump to your instance. THIS DESTROYS THE CURRENT DB! (if there is one)
heroku pg:backups:restore --app ${INSTANCE_NAME} "${DUMP_URL}" DATABASE_URL

# set config vars
heroku config:set --app ${INSTANCE_NAME} TZ="Europe/Paris"
heroku config:set --app ${INSTANCE_NAME} DEBUG=True
# used for what?? Cannot be empty.
heroku config:set --app ${INSTANCE_NAME} SECRET_KEY="<your secret key>"
heroku config:set --app ${INSTANCE_NAME} CELERY_BROKER_URL=ignore

# mail settings
heroku config:set --app ${INSTANCE_NAME} DEFAULT_FROM_EMAIL=e-controle-beta@ccomptes.fr
# Gmail : create or reuse a gmail account.
# You will have to authorize less secure apps, otherwise gmail refuses the connection.
# https://myaccount.google.com/lesssecureapps
heroku config:set --app ${INSTANCE_NAME} EMAIL_HOST_USER=<your email>@gmail.com
heroku config:set --app ${INSTANCE_NAME} EMAIL_HOST_PASSWORD='<your password>'
heroku config:set --app ${INSTANCE_NAME} EMAIL_HOST=smtp.gmail.com
heroku config:set --app ${INSTANCE_NAME} EMAIL_PORT=465
heroku config:set --app ${INSTANCE_NAME} EMAIL_USE_TLS=True
heroku config:set --app ${INSTANCE_NAME} EMAIL_USE_SSL=True


# Instance's postgres url
DB_URL="$(heroku pg:credentials:url --app ${INSTANCE_NAME} DATABASE_URL | grep 'postgres://')"
heroku config:set --app ${INSTANCE_NAME} DATABASE_URL="${DB_URL}"
# not sure what that's for
heroku config:set --app ${INSTANCE_NAME} STAGING_DATABASE_URL=postgres://ijrphgdxjsfyyl:6311267c9240ee54d933f745d4343724eddea476b2be271c6d93477987a1ee3c@ec2-79-125-124-30.eu-west-1.compute.amazonaws.com:5432/d150jki8bk56cd

# Add node buildpack, so that the frontend code gets built. The python buildback should be automatically installed by heroku.
heroku buildpacks:set --app ${INSTANCE_NAME} heroku/nodejs

# All done!

# Next steps :
# push code : it triggers deployment
# git remote add heroku git@heroku.com:"${INSTANCE_NAME}".git # if you already have a remote named heroku, use another name
# git push heroku <local branch to push>:master # you have to push to heroku's master branch, the other branches are ignored

# Log in with admin user
# Modify the URL of the site in the DB, so that the links in emails point to the right URL
# https://my-instance-name.herokuapp.com/admin/sites/site/

# All done!
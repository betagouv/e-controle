#!/bin/sh
: "${HEROKU_APP_NAME?Need to set HEROKU_APP_NAME}"

if  [[ $HEROKU_APP_NAME != *-pr-* ]] ;
then
    echo "Not a PR"
    exit 1
fi

psql -t -c "select 'drop table if exists \"' || tablename || '\" cascade;'
        from pg_tables
       where schemaname = 'public'; " $DATABASE_URL | psql $DATABASE_URL

pg_dump -x -O --if-exists --clean $STAGING_DATABASE_URL | psql $DATABASE_URL
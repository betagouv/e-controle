FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV PORT 8000

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client gettext curl openssh-server

COPY ./ecc /code
COPY ./heroku /code/heroku
RUN mkdir -p /app/.profile.d
RUN echo '[ -z "$SSH_CLIENT" ] && source <(curl --fail --retry 3 -sSL "$HEROKU_EXEC_URL")' > /app/.profile.d/heroku-exec.sh
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

WORKDIR /code

RUN pip install -r requirements.txt

COPY ./docker/django/docker-entrypoint.sh /
COPY ./docker/django/uwsgi.ini /uwsgi.ini.template
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["uwsgi", "--ini", "/uwsgi.ini"]

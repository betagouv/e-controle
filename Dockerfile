FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV PORT 8000

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client gettext

COPY ./ecc /code

WORKDIR /code

RUN pip install -r requirements.txt

COPY ./docker/django/docker-entrypoint.sh /
COPY ./docker/django/uwsgi.ini /uwsgi.ini.template
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["uwsgi", "--ini", "/uwsgi.ini"]

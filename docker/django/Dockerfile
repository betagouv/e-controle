FROM python:3.6

ENV PYTHONUNBUFFERED 1

COPY ./ecc /code

COPY ./database/ /database/

WORKDIR /code

RUN pip install -r requirements.txt

COPY ./docker/django/docker-entrypoint.sh /

RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["python", "manage.py", "runserver", "0:80"]

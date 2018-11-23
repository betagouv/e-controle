FROM centos:centos7

ENV PYTHONUNBUFFERED 1
ENV PORT 8000

RUN yum -y update; yum clean all
RUN yum -y install epel-release centos-release-scl; yum clean all
RUN yum -y install python36 python36-devel python36-setuptools; yum clean all
RUN yum -y groupinstall "Development Tools"; yum clean all
RUN easy_install-3.6 pip
RUN rpm -Uvh https://yum.postgresql.org/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm
RUN yum -y install postgresql10-client gettext; yum clean all

RUN yum -y install curl openssh-server; yum clean all

COPY ./ecc /code
COPY ./heroku /code/heroku
RUN mkdir -p /app/.profile.d
RUN echo '[ -z "$SSH_CLIENT" ] && source <(curl --fail --retry 3 -sSL "$HEROKU_EXEC_URL")' > /app/.profile.d/heroku-exec.sh
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

WORKDIR /code

RUN pip3 install -r requirements.txt

COPY ./docker/django/docker-entrypoint.sh /
COPY ./docker/django/uwsgi.ini /uwsgi.ini.template
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["uwsgi", "--ini", "/uwsgi.ini"]

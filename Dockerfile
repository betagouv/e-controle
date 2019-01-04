FROM centos:centos7

ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# Python
RUN yum -y update; yum clean all
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
RUN yum -y install epel-release; yum clean all
RUN yum -y install python36u python36u-pip python36u-devel python36u-setuptools; yum clean all
RUN yum -y groupinstall "Development Tools"; yum clean all
RUN easy_install-3.6 pip

# PostgreSQL
RUN rpm -Uvh https://yum.postgresql.org/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm
RUN yum -y install postgresql10 gettext; yum clean all

# App
COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

COPY /docker-entrypoint.sh /
COPY ./uwsgi.ini /
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["uwsgi", "--ini", "/uwsgi.ini"]

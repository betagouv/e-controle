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

# Locales
RUN localedef -c -f UTF-8 -i fr_FR fr_FR.UTF-8

# App
COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

RUN chmod +x docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/app/docker-entrypoint.sh"]

FROM centos:centos7

ENV PYTHONUNBUFFERED 1
ENV PORT 8080

# PostgreSQL, client only. Useful for CLI operations on the DB.
RUN rpm -Uvh https://yum.postgresql.org/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm
RUN yum -y install postgresql10; yum clean all

# Python
RUN yum -y update; yum clean all
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
RUN yum -y install epel-release; yum clean all
RUN yum -y install python36u python36u-pip python36u-devel python36u-setuptools; yum clean all
RUN yum -y groupinstall "Development Tools"; yum clean all
RUN easy_install-3.6 pip

# Node.js and NPM
RUN curl -sL https://rpm.nodesource.com/setup_10.x | bash -
RUN yum -y install nodejs; yum clean all

# Make python3 the default
RUN ln -fs /usr/bin/python3.6 /usr/bin/python

# Locales
RUN localedef -c -f UTF-8 -i fr_FR fr_FR.UTF-8

# App
COPY . /app
WORKDIR /app

# Python and NPM Packaging
RUN pip3 install -r requirements.txt
RUN npm install

RUN chmod +x docker-entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/app/docker-entrypoint.sh"]

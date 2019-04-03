# e-controle
Outil permettant de simplifier la relation entre un organisme de contrôle et des structures contrôlés.

## Prérequis

- Nous utilisons [Docker](https://www.docker.com/) pour installer l'environnement de dévelopement
- Nous utilisons [git-flow](https://nvie.com/posts/a-successful-git-branching-model/). Il existe
  une extention git permet de standardiser ce process: https://danielkummer.github.io/git-flow-cheatsheet/

Autres technos utilisées (pas besoin de les installer localement, elles sont sur docker):
 - python
 - Django

## Présentation des services
Nous utilisons deux containers Dockers : un pour postgres, un pour django (définis dans https://github.com/betagouv/e-controle/blob/develop/docker-compose.yml).

Le container postgres a une image standard, le django une image faite maison (défini par la https://github.com/betagouv/e-controle/blob/develop/Dockerfile).

Quand on lance le container django avec `docker-compose run django`, il commence par exécuter https://github.com/betagouv/e-controle/blob/develop/docker-entrypoint.sh. Ce script source l'environnement, migre la base postgres si necessaire, puis exécute une commande si elle est donnée (par exemple la commande `dev`, avec `docker-compose run django dev`, lance le serveur django.).

Le filesystem de la machine hôte est partagé avec le container django : le dossier `.` en local (root du repo github) est le même que le dossier `\app` sur le container. Les modifs en local apparaissent dans le container sans le relancer.

## Variables d'environnement

Certaines variables d'environnement doivent être positionnées pour que l'application fonctionne.

On définit les variables d'environnement dans le fichier `.env`.
On peut utiliser le fichier d'example comme ceci:

    cd /project/folder/
    cp .env.sample .env

Les variables d'environnement sont automatiquement intégrées au process uWSGI via
le fichier `ecc/wsgi.py` - de même pour le fichier `ecc/manage.py`.

## Lancement en dev avec docker-compose

Créer le fichier avec les variables d'environnement :

    cp .env.sample .env

Optionnel, mais pratique : configurer l'envoi de mails.
Les users non-admin n'ont pas de mot de passe, ils recoivent un lien par mail pour se logger. Sans config mail, vous ne pourrez utiliser que des users admin (avec mot de passe, depuis l'interface admin : `<server url>/admin`).
 - Se créer un compte sur debug mail : https://debugmail.io
 - Les informations de connection SMTP se trouve dans les "settings" de debugmail
 - Modifier `.env` avec les informations de connection SMTP

Builder l'image Docker pour django (`build` utilise la `Dockerfile`):

     docker-compose build

Lancer le container `django`, et lui passer la commande `dev`. Comme le container postgres est défini comme un dépendance (voir `links` dans docker-compose.yml), il est lancé aussi.

    docker-compose django dev

On doit pouvoir se connecter au serveur django, en utilisant soit :
 - (linux only, ne marche pas sur macos) l'adresse IP et le numéro de port du serveur qui s'affiche sur le terminal. Par example : http://172.18.0.3:8080/admin/
 - le port forwarding. Pour cela, lancer le serveur avec le flag `-p` : `docker-compose run -p 8080:8080 django dev`. On peut accéder sur le port 8080 de localhost, qui forwarde au port 8080 du container django : http://localhost:8080/admin


## Restaurer/Sauvegarder la base de données en dev

Pour se connecter à postgres, une méthode simple est de lancer un autre container, depuis lequel on se connecte à postgres. Par exemple le container `django`, sans la commande `dev` (on ne lance pas le serveur), avec la commande `bash` pour obtenir un terminal :

    docker-compose run django bash

Ensuite charger le dump dans la base :

    psql -h postgres -U ecc -d ecc < db.dump

Le mot de passe est `ecc` (défini dans docker-compose.yml)

Voilà des utilisateurs admin qui existent par défaut quand on utilise le dump de démo:
- inspector@demo.com / demoe12345
- audited@demo.com / demoe12345

Note : Comment le dump a été créé :

    pg_dump --verbose --clean --no-acl --no-owner -h postgres -U ecc -d ecc > db.dump



## Des comamndes utiles

    docker-compose run django dev
    docker-compose run django uwsgi
    docker-compose run django python3.6 manage.py runserver 0:8080
    docker-compose run django python3.6 manage.py shell_plus
    docker-compose run django <any-command>
    docker-compose up -d

    # lancer les tests unitaires sur un container django :
    docker-compose run django bash # l'environnement est sourcé par le docker-entrypoint.sh
    pytest


## Lancement en prod

- Une base PostgreSQL 10 doit être fournie.


## Définition des locales

Cette plateforme utilise l'encodage UTF-8 à plusieurs endroit, notament pour les nom de
fichiers uploadés.

Pour que cela fonctionne, il faut rendre configurer correctement les 'locales',
par example comme ceci:

    localedef -c -f UTF-8 -i fr_FR fr_FR.UTF-8
    export LANG=fr_FR.UTF-8
    export LC_ALL=fr_FR.UTF-8

## Envoi d'emails périodiques

On utilise Celery Beat et Redis pour gérer l'envoi d'emails périodiques.

La fréquence des envois est configurée dans django admin, avec l'applicaiton 'django_celery_beat'.

Pour démarrer celery beat, il y a la commande suivante:


    celery worker --beat -A ecc -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &


Un autre façon de faire, est d'installer un service systemd:


    ln -s /opt/e-controle/deploy/conf/celery.service /etc/systemd/system/celery.service
    systemctl daemon-reload
    systemctl start celery
    systemctl restart status
    tail /var/log/ecc-celery.log


Si le serveur Redis n'est pas fournit, on peut l'installer:


    yum -y install redis
    systemctl start redis
    systemctl enable redis
    redis-cli ping

## uWSGI
Todo : c'est quoi, comment ca marche, ...


## Travailler avec Parcel

Nous avons fait le choix d'utiliser le bundler parcel qui est une alternative à Webpack.

Pour lancer le build en mode wach:

    docker-compose run django watch

Quelques commandes bash utiles:

    npm install  # Pour installer les dépendences
    npm run build  # Pour construire le fichier bundle
    npm run watch  # Pour construire le fichier bundle en mode watch

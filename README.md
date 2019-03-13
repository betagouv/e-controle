# e-controle
Outil permettant de simplifier la relation entre un organisme de contrôle et des structures contrôlés.

## Lancement en dev avec docker-compose

    cd e-control
    cp .env.sample .env
    docker-compose build
    docker-compose up -d
    docker-compose run django dev

L'addresse IP et le numéro de port du server devrait s'afficher sur le terminal et permet de
se connecter à l'admin:

Par example : http://172.18.0.3:8080/admin/


## Restaurer/Sauvegarder la base de données en dev

    psql -h postgres -U ecc -d ecc < db.dump

Pour créer le dump:

    pg_dump --verbose --clean --no-acl --no-owner -h postgres -U ecc -d ecc > db.dump

Le mot de passe par de demo est `ecc`.


## Comment se connecter en tant que dev

En tant que dev, dans l'environnement local, il n'est pas toujours possible de s'envoyer un email
pour se conneter.

Dans ce cas, avant d'aller à la racine du site "/", on peut d'abord passer par le login
de l'interface d'admin "/admin/"


Voilà des utilisateurs qui existent par défaut quand on utilise le dump de démo:

- inspector@demo.com / demoe12345
- audited@democom / demoe12345


## Des comamndes utiles

    docker-compose run django dev
    docker-compose run django uwsgi
    docker-compose run django bash
    docker-compose run django python3.6 manage.py runserver 0:8080
    docker-compose run django python3.6 manage.py shell_plus
    docker-compose run django <any-command>


## Lancement en prod

- Une base PostgreSQL 10 doit être fournie.

## Variables d'environnement

Certaines variables d'environnement doivent être positionnées pour que l'application fonctionne.

On défini les variables d'environnement dans le fichier `.env`.
On peut utiliser le fichier d'example comme ceci:

    cd /project/folder/
    cp .env.sample .env

Les variables d'environnement sont automatiquement intégrées au process uWSGI via le fichier `ecc/wsgi.py`.


## Définition des locales

Cette plateforme utilise l'encodage UTF-8 à plusieurs endroit, notament pour les nom de
fichiers uploadés.

Pour que cela fonctionne, il faut rendre configurer correctement les 'locales',
par example comme ceci:

    localedef -c -f UTF-8 -i fr_FR fr_FR.UTF-8
    export LANG=fr_FR.UTF-8
    export LC_ALL=fr_FR.UTF-8

## Envoie d'emails périodiques

On utilise Celery Beat et Redis pour gérer l'envoie d'emails périodiques.

La fréquence des envoies est configurée dans django admin, avec l'applicaiton 'django_celery_beat'.

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

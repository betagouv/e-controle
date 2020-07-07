# Environnement de développement
## Principes
Nous utilisons [git-flow](https://nvie.com/posts/a-successful-git-branching-model/). Il existe
  une extention git permet de standardiser ce process: https://danielkummer.github.io/git-flow-cheatsheet/

Notre code review process pour collaborer dans la bonne humeur :
https://docs.google.com/document/d/1N3ulNnQYNUhoizEeBYqnp2ndeRYn8_QKjxQS5pQmVmQ/edit

## Variables d'environnement

Certaines variables d'environnement doivent être positionnées pour que l'application fonctionne.

On définit les variables d'environnement dans le fichier `.env`.
On peut utiliser le fichier d'example comme ceci:

    cd /my/project/folder/
    cp .env.sample .env

Les variables d'environnement sont automatiquement intégrées au process uWSGI via
le fichier `ecc/wsgi.py` - de même pour le fichier `ecc/manage.py`.


# Environnement de développement avec Docker
On peut utiliser Docker pour gagner du temps d'installation. Par contre ca utilise plus de mémoire. C'est un choix!

Si vous ne voulez pas utiliser Docker, voir le paragraphe suivant.

## Prérequis

- Nous utilisons [Docker](https://www.docker.com/) pour installer l'environnement de dévelopement

Autres technos utilisées (pas besoin de les installer localement, elles sont sur docker):
 - Python
 - Django


## Présentation des containers
Nous utilisons deux containers Dockers : un pour postgres, un pour django (définis dans https://github.com/betagouv/e-controle/blob/develop/docker-compose.yml).

Le container postgres a une image standard, le django une image faite maison (défini par la https://github.com/betagouv/e-controle/blob/develop/Dockerfile).

Quand on lance le container django avec `docker-compose run django`, il commence par exécuter https://github.com/betagouv/e-controle/blob/develop/docker-entrypoint.sh. Ce script source l'environnement, migre la base postgres si necessaire, puis exécute une commande si elle est donnée (par exemple la commande `dev`, avec `docker-compose run django dev`, lance le serveur django.).

Le filesystem de la machine hôte est partagé avec le container django : le dossier `.` en local (root du repo github) est le même que le dossier `\app` sur le container. Les modifs en local apparaissent dans le container sans le relancer.

## Notre Docker Django

L'image docker pour Django peut être construite à partir de plusieurs images :

- sur la base d'une image Centos
- sur la base une image Python/Node

Pour changer l'image de base, il faut changer l'option `dockerfile` specifiée dans `docker-compose.yml`.

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

# Environnement de développement sans Docker

Surtout utile si Docker utilise trop de mémoire (2 GB). C'est aussi plus simple pour connecter un IDE (comme VSCode ou autre).

## Postgres
Suivre ce tutorial pour installer postgres, et créer un user nommé `ecc` et une database nommée `ecc`.
https://tutorial-extensions.djangogirls.org/en/optional_postgresql_installation/

Loader le dump dans la base de données qu'on vient de créer : voir paragraphe "Restaurer la base de données en dev"

## Node
Installer node et npm.

Installer les dependances node : `npm install`

Builder le front : `npm bun build-all` (pour developper par la suite, on pourra utiliser les commandes `watch` qui rebuildent au fur et à mesure des modifications. Voir `package.json`)

## Python et Django
Installer python 3 (sur mac il y a déja python 2 par default, il faut ajouter python 3 : https://docs.python-guide.org/starting/install3/osx/)

Installer un environnement virtuel python (pipenv ou virtualenv) : https://docs.python-guide.org/dev/virtualenvs/

Installer les dépendences python : `pip install -r requirements.txt`

Dans le fichier `.env`, modifier l'adresse de la db, puis sourcer l'environnement :
```
export DATABASE_URL=postgres://ecc:ecc@localhost:5432/ecc
. .env
```

Migrer la db : `python manage.py migrate`

Collecter les fichiers statiques : `python manage.py collectstatic --noinput`

Lancer le serveur local sur le port 8080 : `python manage.py runserver 0:8080`

Aller sur `http://localhost:8080/admin` et se logger avec un des utilisateurs mentionnés ci-dessous.


# Restaurer/Sauvegarder la base de données en dev

## Docker only : Se connecter à postgres
Pour se connecter à postgres avec l'installation docker, une méthode simple est de lancer un autre container, depuis lequel on se connecte à postgres. Par exemple le container `django`, sans la commande `dev` (on ne lance pas le serveur), avec la commande `bash` pour obtenir un terminal :

    docker-compose run django bash

## Charger le dump dans la base
Ensuite charger le dump dans la base.

Pour l'installation avec docker :

    psql -h postgres -U ecc -d ecc < db.dump

Pour l'installation sans docker :

    psql -h localhost -U ecc -d ecc < db.dump

Le mot de passe est `ecc` (défini dans docker-compose.yml pour Docker, et créé plus haut si pas de Docker)

Voilà des utilisateurs admin qui existent par défaut quand on utilise le dump de démo:
- Admin: admin@demo.com / demo12345
- Controlé: robert@demo.com / demo12345
- Contrôleur: martine@demo.com / demo12345

Note : Pour créer un nouveau dump :

    pg_dump --verbose --clean --no-acl --no-owner -h postgres -U ecc -d ecc > db.dump

Ensuite, ajouter dezipper les fichiers de `media.zip` dans un dossier `media` à la racine de ce projet.

# Login et envoi d'emails

Les utlisateurs admin peuvent se logger sans envoi d'email à http://localhost:8080/admin.
(Si vous avez utilisé le dump ci-dessus, essayez admin@demo.com / demo12345)

Les utilisateurs non-admin n'ont pas de mot de passe, ils recoivent un email contenant un lien de connexion. Votre serveur doit donc être configuré pour envoyer des mails.

## Serveur d'email en local
Python contient un petit serveur SMTP, qui printe les mail dans la console au lieu de les envoyer. C'est le plus simple pour developper.
Ajoutez les settings suivants dans `.env` :
```
export EMAIL_HOST='localhost'
export EMAIL_PORT=1025
export EMAIL_HOST_USER=''
export EMAIL_HOST_PASSWORD=''
export EMAIL_USE_TLS=False
export DEFAULT_FROM_EMAIL='testing@example.com'
```
Et lancez le serveur :
`python -m smtpd -n -c DebuggingServer localhost:1025`

(Merci à https://gist.github.com/andreagrandi/7027319)

# libmagic
Le serveur Django utilise libmagic (pour vérifier les types des fichiers uploadés), qui doit être présent sur la machine. Vous pouvez essayer de démarrer sans, et si le serveur raise une erreur c'est qu'il faut l'installer à la main sur votre machine.

Instructions d'installation données par django-magic, le package que nous utilisons : https://github.com/ahupp/python-magic#installation


# Des commandes utiles
Pour l'install docker :

    docker-compose run django dev
    docker-compose run django uwsgi
    docker-compose run django python3.6 manage.py runserver 0:8080
    docker-compose run django python3.6 manage.py shell_plus
    docker-compose run django <any-command>
    docker-compose up -d

    # lancer les tests unitaires sur un container django :
    docker-compose run django bash # l'environnement est sourcé par le docker-entrypoint.sh
    pytest


# Lancement en prod

- Une base PostgreSQL 10 doit être fournie.


# Définition des locales

Cette plateforme utilise l'encodage UTF-8 à plusieurs endroit, notament pour les nom de
fichiers uploadés.

Pour que cela fonctionne, il faut rendre configurer correctement les 'locales',
par example comme ceci:

    localedef -c -f UTF-8 -i fr_FR fr_FR.UTF-8
    export LANG=fr_FR.UTF-8
    export LC_ALL=fr_FR.UTF-8

# Envoi d'emails périodiques

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

# uWSGI
Le server d'application uWSGI est utilisé sur Heroku.
Pour plus de détail : https://uwsgi-docs.readthedocs.io/en/latest/

# Parcel : Bundler JS

Nous avons fait le choix d'utiliser le bundler parcel qui est une alternative à Webpack.
Voir le fichier ``package.json`` pour plus de détails.

Quelques commandes bash utiles:

    npm install  # Pour installer les dépendences

    npm run build-all

    npm run watch-control-detail  # Pour construire le fichier bundle en mode watch
    npm run build-control-detail  # Pour construire le fichier bundle

    npm run watch-questionnaire-create
    npm run watch-questionnaire-detail
    npm run watch-session-management

# Tests

## Backend tests

Lancer les tests :
`pytest -s <dossier>`
(le flag -s sert a laisser le debugger prendre le controle si besoin).


## Frontend tests
Ils se situent dans `static/src/` avec le code, dans des dossiers `test`. Ce sont des tests Jest, pour trouver de la doc googler "test Vue with Jest" par exemple.

Lancer les tests : `npm test`

Tester un fichier en particulier :

`npm test <tout ou partie du nom de fichier>`.

Par exemple : `npm test Metadata` trouve le fichier `static/src/questionnaires/test/QuestionnaireMetadataCreate.spec.js`.

Debugger un test : plusieurs debuggers sont possibles, dont Chrome Dev Tools et Webstorm/Pycharm. Voir https://jestjs.io/docs/en/troubleshooting

Pour VScode, il y a une config pour debugger directement dans l'éditeur : `.vscode/launch.json`. La config s'appelle "Debug Jest Tests". Pour la lancer : ![image](https://user-images.githubusercontent.com/911434/72448689-ba28cb80-37b7-11ea-84b8-635040f8eaf1.png)
Ou voir la doc plus complète de VScode : https://code.visualstudio.com/docs/editor/debugging

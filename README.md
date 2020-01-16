# e-controle
“e.contrôle” est un service numérique permettant de faciliter les échanges de documents durant les contrôles, audits ou inspections.

Les activités de transmission et de réception de documents durant les audits ne sont facilitées par aucun outil suffisamment adapté, si bien qu’une marge d’optimisation existe. 

e.contrôle propose de répondre aux nombreux problèmes rencontrés par les audités et les auditeurs.

La mise en place d’un outil dédié permet de simplifier la relation entre un organisme de contrôle et des structures contrôlées afin de leur permettre de se concentrer sur les activités ayant le plus d’impact pour leurs usagers.

## Les principaux gains pour les utilisateurs :
- Des tâches pénibles en moins : les centaines ou milliers de fichiers de réponses aux questionnaires sont classés et renommés automatiquement. Plus aucun agent n’a besoin d’y passer des heures.
- De l’autonomie : les équipes de contrôle ne sont dépendantes d’aucun autre service pour créer des espaces de dépôts ou des comptes utilisateurs. Elles n’ont plus besoin d’attendre 24 ou 48h.
- Du stress en moins : l’interface simplifiée est compréhensible pour le plus grand nombre, quel que soit le niveau de familiarité avec l’informatique.

### Captures d'écran :
- Page de connexion
![Page de connexion](https://user-images.githubusercontent.com/43180136/72534189-ad1ee180-3876-11ea-8ebc-79ec6cf13172.JPG)

- Exemple fictif d'un espace de dépôt
![Exemple fictif d'un espace de dépôt](https://user-images.githubusercontent.com/43180136/72534844-cecc9880-3877-11ea-8d20-02ce808cd56c.JPG)

- Exemple fictif d'un questionnaire (vue contrôleur)
![Exemple fictif d'un questionnaire](https://user-images.githubusercontent.com/43180136/72534971-089d9f00-3878-11ea-9461-d2a1baf0c544.JPG)

- Exemple fictif d'un questionnaire pour déposer des réponses (vue contrôlé)
![exemple depot fichiers](https://user-images.githubusercontent.com/43180136/72535583-14d62c00-3879-11ea-9e17-d522073bf937.JPG)

- Arborescence des fichiers déposés automatiquement classés et renommés
![econtrole3](https://user-images.githubusercontent.com/43180136/72535271-8f527c00-3878-11ea-8ece-6d57b44b8a51.png)

### Rapide apperçu d'e.contrôle en vidéo :

#### Pour toutes les équipes de contrôle et les organismes interrogés:

- ["Je me connecte"](https://drive.google.com/file/d/1QKhy3A6xJBDOoSWj8F-Qh9z9A0cJxx5K/view)

#### Pour les équipes de contrôle

- ["Je crée un espace de dépôt"](https://drive.google.com/open?id=1h_jtT6hSwTNNgWfL7LFWZjRpPPmsvhah=)
- ["J'ajoute un membre de mon équipe de contrôle à un espace de dépôt"](https://drive.google.com/open?id=1P3BT-ANF39P3k7fBkiz8RYwtUNo3rmKR)

- ["Je crée un questionnaire"](https://drive.google.com/open?id=153O1s1O3SgilUwvXnZDY-v9t84pOOPUh)
- ["Je modifie puis publie un questionnaire"](https://drive.google.com/open?id=1uNW5W1DHBkHKMzlM1Pt4SSxxxlP3Tc6v)
- ["J'ajoute un accès à un agent d'un organisme interrogé"](https://drive.google.com/open?id=1rUlFlvT_4T-sxvwhb2-Q3Wdrw59ycvxW)
- ["Je consulte les réponses déposées"](https://drive.google.com/open?id=1mvntyQ0TwET-ENb_xRbc32RiAKu2KnBn)

- ["J'explore les réponses dans mon explorateur de fichiers windows"](https://drive.google.com/open?id=1rzZ5LqJnMkHTjmYajHxvZqDyqHafRQL9)

#### Pour les agents des organismes interrogés

- ["Je dépose des documents de réponse à une question"](https://drive.google.com/open?id=1KPcRKKeS_HriJpciNE6GZmiuIF5OA-y2)


Les descriptions fonctionnelles sont disponibles [ici](https://docs.google.com/document/d/1ETBSoGE-oSOqgq-bR2M3v3SsRAJ6L_R1t0SMcwWSwsI/edit?usp=sharing).

## Architecture du code et du repo
Voir https://github.com/betagouv/e-controle/blob/develop/docs/dev/devdoc.md

## Environnement de développement
### Prérequis

- Nous utilisons [Docker](https://www.docker.com/) pour installer l'environnement de dévelopement
- Nous utilisons [git-flow](https://nvie.com/posts/a-successful-git-branching-model/). Il existe
  une extention git permet de standardiser ce process: https://danielkummer.github.io/git-flow-cheatsheet/

Autres technos utilisées (pas besoin de les installer localement, elles sont sur docker):
 - Python
 - Django

Notre code review process pour collaborer dans la bonne humeur :
https://docs.google.com/document/d/1N3ulNnQYNUhoizEeBYqnp2ndeRYn8_QKjxQS5pQmVmQ/edit

### Présentation des services
Nous utilisons deux containers Dockers : un pour postgres, un pour django (définis dans https://github.com/betagouv/e-controle/blob/develop/docker-compose.yml).

Le container postgres a une image standard, le django une image faite maison (défini par la https://github.com/betagouv/e-controle/blob/develop/Dockerfile).

Quand on lance le container django avec `docker-compose run django`, il commence par exécuter https://github.com/betagouv/e-controle/blob/develop/docker-entrypoint.sh. Ce script source l'environnement, migre la base postgres si necessaire, puis exécute une commande si elle est donnée (par exemple la commande `dev`, avec `docker-compose run django dev`, lance le serveur django.).

Le filesystem de la machine hôte est partagé avec le container django : le dossier `.` en local (root du repo github) est le même que le dossier `\app` sur le container. Les modifs en local apparaissent dans le container sans le relancer.


### Notre Docker Django

L'image docker pour Django peut être construite à partir de plusieurs images :

- sur la base d'une image Centos
- sur la base une image Python/Node

Pour changer l'image de base, il faut changer l'option `dockerfile` specifiée dans `docker-compose.yml`.


### Variables d'environnement

Certaines variables d'environnement doivent être positionnées pour que l'application fonctionne.

On définit les variables d'environnement dans le fichier `.env`.
On peut utiliser le fichier d'example comme ceci:

    cd /project/folder/
    cp .env.sample .env

Les variables d'environnement sont automatiquement intégrées au process uWSGI via
le fichier `ecc/wsgi.py` - de même pour le fichier `ecc/manage.py`.

### Lancement en dev avec docker-compose

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

### Lancement en dev sans docker

Surtout utile si Docker utilise trop de mémoire (2 GB).

### Postgres
Suivre ce tutorial pour installer postgres, et créer un user nommé `ecc` et une database nommée `ecc`.
https://tutorial-extensions.djangogirls.org/en/optional_postgresql_installation/

Loader le dump dans la base de données qu'on vient de créer : voir paragraphe "Restaurer la base de données en dev"

### Node
Installer node et npm.

Installer les dependances node : `npm install`

Builder le front : `npm bun build-all` (pour developper par la suite, on pourra utiliser les commandes `watch` qui rebuildent au fur et à mesure des modifications. Voir `package.json`)

### Python et Django
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


### Restaurer/Sauvegarder la base de données en dev

Pour se connecter à postgres avec l'installation docker, une méthode simple est de lancer un autre container, depuis lequel on se connecte à postgres. Par exemple le container `django`, sans la commande `dev` (on ne lance pas le serveur), avec la commande `bash` pour obtenir un terminal :

    docker-compose run django bash

Ensuite charger le dump dans la base :

    psql -h postgres -U ecc -d ecc < db.dump

(si l'installation postgres est locale, sans docker, utiliser `localhost` au lieu de `postgres` dans la commande)

Le mot de passe est `ecc` (défini dans docker-compose.yml)

Voilà des utilisateurs admin qui existent par défaut quand on utilise le dump de démo:
- Controlé: robert@demo.com / demo12345
- Contrôleur: martine@demo.com / demo12345

Note : Pour créer un nouveau dump :

    pg_dump --verbose --clean --no-acl --no-owner -h postgres -U ecc -d ecc > db.dump

Ensuite, ajouter dezipper les fichiers de `media.zip` dans un dossier `media` à la racine de ce projet.

### Login et envoi d'emails

Les utlisateurs admin peuvent se logger sans envoi d'email à http://localhost:8080/admin.
(Si vous avez utilisé le dump ci-dessus, essayez admin@demo.com / demo12345)

Les utilisateurs non-admin n'ont pas de mot de passe, ils recoivent un email contenant un lien de connexion. Votre serveur doit donc être configuré pour envoyer des mails.

#### Serveur d'email en local
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

### Des commandes utiles

    docker-compose run django dev
    docker-compose run django uwsgi
    docker-compose run django python3.6 manage.py runserver 0:8080
    docker-compose run django python3.6 manage.py shell_plus
    docker-compose run django <any-command>
    docker-compose up -d

    # lancer les tests unitaires sur un container django :
    docker-compose run django bash # l'environnement est sourcé par le docker-entrypoint.sh
    pytest


### Lancement en prod

- Une base PostgreSQL 10 doit être fournie.


### Définition des locales

Cette plateforme utilise l'encodage UTF-8 à plusieurs endroit, notament pour les nom de
fichiers uploadés.

Pour que cela fonctionne, il faut rendre configurer correctement les 'locales',
par example comme ceci:

    localedef -c -f UTF-8 -i fr_FR fr_FR.UTF-8
    export LANG=fr_FR.UTF-8
    export LC_ALL=fr_FR.UTF-8

### Envoi d'emails périodiques

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

### uWSGI
Le server d'application uWSGI est utilisé sur Heroku.
Pour plus de détail : https://uwsgi-docs.readthedocs.io/en/latest/

### Parcel : Bundler JS

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

### Tests

#### Backend tests

Lancer les tests :
`pytest -s <dossier>`
(le flag -s sert a laisser le debugger prendre le controle si besoin).


#### Frontend tests
Ils se situent dans `static/src/` avec le code, dans des dossiers `test`. Ce sont des tests Jest, pour trouver de la doc googler "test Vue with Jest" par exemple.

Lancer les tests : `npm test`

Tester un fichier en particulier :

`npm test <tout ou partie du nom de fichier>`.

Par exemple : `npm test Metadata` trouve le fichier `static/src/questionnaires/test/QuestionnaireMetadataCreate.spec.js`.

Debugger un test : plusieurs debuggers sont possibles, dont Chrome Dev Tools et Webstorm/Pycharm. Voir https://jestjs.io/docs/en/troubleshooting

Pour VScode, il y a une config pour debugger directement dans l'éditeur : `.vscode/launch.json`. La config s'appelle "Debug Jest Tests". Pour la lancer : ![image](https://user-images.githubusercontent.com/911434/72448689-ba28cb80-37b7-11ea-84b8-635040f8eaf1.png)
Ou voir la doc plus complète de VScode : https://code.visualstudio.com/docs/editor/debugging

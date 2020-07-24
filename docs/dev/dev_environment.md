# Environnement de développement
## Principes
Nous utilisons [git-flow](https://nvie.com/posts/a-successful-git-branching-model/).
Ce modèle de développement s'appuie deux branches central qui sont *develop* et *master*.
La branche *master* reflète toujours l'état actuel en production, tandis que *develop* pointe sur les
derniers changements opérés en vue de la prochaine release.
Ces deux branches sont les principales branches du projet. Elles sont centralisées et illimitées dans le
temps.

D'autre part, le projet s'articule autour de trois autres types de branches :
 - feature/ ou /bugfix (on peut les utiliser de façon interchangeable, selon qu'on juge qu'on est en train de rajouter une nouvelle fonctionnalité ou de fixer un bug)
 - release/
 - hotfix/

 Ces branches sont appelées branches de support, et elles intéragissent avec les branches principales
 de façon très codifiée. Par exemple :
 - feature/ et /bugfix doivent provenir de *develop* et être mergées dans *develop*
 - release/ doit provenir de *develop* et être mergée dans *develop* et *master*
 - hotfix/ doit provenir de *master* et être mergée dans *develop* et *master*

Par exemple, pour une feature qui fait "Update the user form", on crée une branche de feature en suivant le processus suivant :
```
    $ git checkout develop
    $ git pull
    $ git checkout -b feature/update-user-form develop
```

Le développement de la feature se fait dans la nouvelle branche feature/update-user-form. On peut ajouter autant de commits que necessaire, il est encouragé de committer souvent même pour des versions intermédiaires et moches.

Une fois la feature terminée, il faut incorporer la branche dans develop:
```
    $ git checkout develop
    $ git pull develop
    $ git merge --no-ff feature/update-user-form
    $ git push origin develop
```

Note : Le flag --no-ff (no fast-forward) crée un commit de merge dans la branche develop. Si on ne le met pas, il y a des cas (le cas fast-forward) où tous les commits de la branche feature vont être ajoutés dans develop. Ce n'est pas souhaitable, car la branche feature est une branche de travail, qui peut avoir bcp de commits brouillons et pas interessants à garder. Donc on utilise toujours --no-ff.

Optionnel : supprimer la branche locale. On ne supprime pas la branche remote sur github, pour garder l'historique. (On pourra décider plus tard qu'il y a trop de branches et les supprimer, si c'est nécessaire.)
```
    $ git branch -d feature/update-user-form
```

Pour créer une branche de release (par exemple pour la version 1.20), on suivra le processus suivant :
```
    $ git checkout develop
    $ git pull develop
    $ git checkout -b release/1.20 develop
```

Il y a 2 taches à faire dans cette nouvelle branche (on peut regarder [ce commit](https://github.com/betagouv/e-controle/commit/85a165b8) pour avoir un exemple) :
 - Ajouter des release notes dans le dossier docs/releases. On peut imiter le format des releases precedentes. On peut décider d'un nom pour la release dans ce fichier.
 - Mettre à jour la version affichée sur le site : dans templates/footer.html.

On met ces deux tâches dans un commit dans la branche release/1.20 :
```
    $ git commit -m "Updated version number"
```

Ensuite on teste la release.

On réalise les tests de recette sur au moins 2 navigateurs (3 c'est encore mieux!), dont Intenet Explorer (parce qu'il pose toujours plus de problèmes). Un test de recette doit idéalement cliquer une fois sur chaque bouton de l'interface pour vérifier qu'il marche. On peut suivre la [liste des fonctionnalités à tester](https://docs.google.com/spreadsheets/d/1YAj0BITC4nq3_IDijhncNniTphC55zr3uBrLyzeFE1A/edit#gid=638845062), qui n'est pas exhaustive. On peut aussi tester de façon plus détaillée les parties de l'interface qui ont été modifiées dans la release.

On réalise les tests de recette sur la machine de DEV. Si ils passent (on ne trouve pas de bugs), on déploie en PPROD et on refait les tests de recette en PPROD. Si ils passent, on déploie en PROD.

Dans le cas où les tests de recette trouvent des bugs, il faut les fixer dans la branche release/1.20 puis recommencer le processus de tests.

Pour ajouter le fix dans release/1.20, on peut committer directement dans release/1.20. (Si c'est un gros fix, on peut brancher depuis release/1.20 pour que ca soit plus propre, et ne laisser que le commit de merge dans release/1.20)
```
    $ git commit -m "Fixed bug with the stuff and the things"
```

Une fois que tous les tests sont passés et que la release est déployée en prod, on merge la branche release dans la branche master. La branche master ne contient que des commits qui correspondent à un release.
```
    $ git checkout master
    $ git pull
    $ git merge --no-ff release/1.20
```

On va aussi tagger le commit de master : ca fait apparaitre [une release dans la page de github](https://github.com/betagouv/e-controle/releases), et ca nous permet de garder des traces. On crée le tag en local, puis on le push sur github.
```
    $ git tag -a 1.20
    $ git push origin 1.20
```

Ensuite, il faut "backmerger" dans develop : comme on a ajouté des commits de bugfix dans release/1.20, il faut que ces commits soient ramenés aussi dans develop, pour qu'ils soient présents dans les versions suivantes.
```
    $ git checkout develop
    $ git pull
    $ git merge --no-ff release/1.20
```

Dans le cas où on trouve un bug en prod, après le déploiement, si on décide qu'il est important, on le fixe tout de suite. On fait un hotfix. : c'est une procédure plus rapide que de faire une release complète. Le hotfix se fait directement sur master, sans passer par develop. C'est le seul cas où le code ne commence pas par develop.

Par exemple, on se rend compte que les dates sont affichées en anglais, et on décide que c'est très grave. Pour créer une branche de hotfix, on suivra le processus suivant :
```
    $ git checkout master
    $ git pull
    $ git checkout -b hotfix/fix-dates-in-french
```

On commit le fix dans la branche (ou ou plusieurs commits) :
```
    $ git commit -m "Display the dates in french"
```

Le fix doit aussi changer le numéro de version et faire des release notes pour cette nouvelle version. Si on était précédemment à la version 1.20, alors on fait une version 1.20.1. S'inspirer de [ce commit](https://github.com/betagouv/e-controle/commit/85a165b8) (les release notes sont faciles : il n'y a que le fix qui a changé!)

On déploie cette branche sur heroku ou sur DEV et on teste que le bug est parti. On fait aussi la code review (c'est pas le moment de bacler, ca va aller directement en prod!)

Quand on est satisfait du fix, on merge la branche dans master :
```
    $ git checkout master
    $ git pull
    $ git merge --no-ff hotfix/fix-dates-in-french
```

On déploie master sur la machine de DEV, et on teste que le bug est parti. On n'est pas obligé de refaire tous les tests de recette. Ensuite on déploie sur pprod et on reteste. S'il y a encore des problèmes on les fixe.

Ensuite on fait un déploiement en prod.

On tagge master pour garder un historique des releases :
```
    $ git checkout master
    $ git pull
    $ git tag -a 1.20.1
    $ git push origin 1.20.1
```

Et on backmerge dans develop.
```
    $ git checkout develop
    $ git pull
    $ git merge --no-ff release/1.20.1
```

...

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

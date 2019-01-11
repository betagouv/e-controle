# e-controle
Outil permettant de simplifier la relation entre un organisme de contrôle et des structures contrôlés

# Lancement en prod
- Une base PostgreSQL 10 doit être fournie.

# Lancement en dev avec docker-compose
- Le docker-compose.yml est fourni pour le développement uniquement.
- Usage : `docker-compose up`


# Variables d'environnement

Certaines variables d'environnement doivent être positionnées pour que l'application fonctionne.

On défini les variables d'environnement dans le fichier `.env`.
On peut utiliser le fichier d'example comme ceci:

    cd /project/folder/
    cp .env.sample .env

Les variables d'environnement sont automatiquement intégrées au process uWSGI via le fichier `ecc/wsgi.py`.

# Restaurer le dump de la base de données en dev

    cd $CODE_DIR/deploy/
    gpg latest.dump.gpg
    pg_restore --verbose --clean --no-acl --no-owner -h postgres -U ecc -d ecc latest.dump

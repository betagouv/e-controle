# e-controle
Outil permettant de simplifier la relation entre un organisme de contrôle et des structures contrôlés

# Lancement en prod
- Un Dockerfile est présent pour le mettre en prod.
- Une base PostgreSQL 10 doit être fournie.
- Variables d'environnement dans le contexte docker necessaires :
  - SECRET_KEY : chaîne aléatoire de 50 caractères libres
  - DATABASE_URL : URL de connexion à la base de données. Format : postgres://user:password@ip:5432/db_name
- Variable optionnel :
  - PORT : par défaut 8000
  - DEBUG : pour mettre django en mode débug (par défaut False)

# Lancement en dev avec docker-compose
- Le docker-compose.yml est fourni pour le développement uniquement.
- Usage : `docker-compose up`


# Variables d'environnement

Certaines variables d'environnement doivent être positionnées pour que l'application fonctionne.

On défini les variables d'environnement dans le fichier `ecc/.env`.
On peut utiliser le fichier d'example comme ceci:

    cd /project/folder/
    cp .env.sample .env

Les variables d'environnement sont automatiquement intégrées au process uWSGI via le fichier `ecc/wsgi.py`.

## Virtialenv

Pour intégrer ces variable dans le virtalenv, on peu itiliser le script `postactivate` qui est lancé après l'activation du virtualenv.

    echo 'set -a; source /project/folder/.env; set +a' >> /path/to/virtualenv/bin/postactivate

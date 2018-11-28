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

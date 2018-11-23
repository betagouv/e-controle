# e-controle
Outil permettant de simplifier la relation entre un organisme de contrôle et des structures contrôlés

# Lancement en prod
- Un Dockerfile est présent pour le mettre en prod.
- Une base PostgreSQL 10 doit être fournit.
- Variables d'environnement dans le context docker necessaires :
  - SECRET_KEY : chaine aléatoire de 50 caractères libre
  - DATABASE_URL : URL de connection à la base de donnée. Format : postgres://user:password@ip:5432/db_name
- Variable optionnel :
  - PORT : par défaut 8000
  - DEBUG : pour mettre django en mode débug (par défaut False) 

# Lancement en dev avec docker-compose
- Le docker-compose.yml est fournit pour le développement uniquement.
- Usage : `docker-compose up`

#!/bin/sh

# Ajout de la nouvelle version du code sur la machine

source $VENV_DIR/bin/activate

cd $PROJECT_DIR
git pull
pip install -r requirements.txt
python3.6 ./manage.py migrate
python3.6 ./manage.py collectstatic --noinput

# Ajout des certificats SSL dans le repertoire /etc/ssl/

# Changement des configurations apache
# Copier les configurations de /deploy/conf/*.conf vers /etc/httpd/conf.d/
# Modifier le noms des variables dans les configurations (Variable $URL $PROTOCOL+$URL $CRT_PATH $PEM_CRT)
# Verifier que les variables d'environnement relatives à la connexion ldap dans le .env sont bien complétées.
# Relancer apache
systemctl restart httpd
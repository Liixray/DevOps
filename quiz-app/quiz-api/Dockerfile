# Image de l'API basée sur python
FROM python:3.13-slim

# Répertoire de travail
WORKDIR /app

# Dépendances
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Ne pas créer de fichier SQLite ici — nous utilisons MySQL en conteneur.
# (La création d'un fichier SQLite local pourrait amener l'app à l'utiliser par erreur.)

# Variables d'environnement de prod
ENV FLASK_DEBUG=0
ENV FLASK_ENV=production
ENV FLASK_APP=app.py

# Code de l'app
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Métadonnées (optionnelles)
LABEL maintainer="Mahnane Nassim <mahnane.nassim@edu-esiee.fr>" \
      version="1.0"

# Lancement via Gunicorn
ENTRYPOINT ["/entrypoint.sh"]

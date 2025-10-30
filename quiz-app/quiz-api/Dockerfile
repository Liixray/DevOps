# Image de l'API basée sur python
FROM python:3.13-slim

# Répertoire de travail
WORKDIR /app

# Dépendances
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Base SQLite vide
RUN touch quiz.db

# Variables d'environnement de prod
ENV FLASK_DEBUG=0
ENV FLASK_ENV=production
ENV FLASK_APP=app.py

# Code de l'app
COPY . .

# Métadonnées (optionnelles)
LABEL maintainer="Mahnane Nassim <mahnane.nassim@edu-esiee.fr>" \
      version="1.0"

# Lancement via Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--log-level", "info", "--error-logfile", "-", "--access-logfile", "-"]

# Quiz App – Architecture & Guide

## Statuts CI/CD

![Tests & Build API](https://github.com/DevOpsQuizz/DevOps/actions/workflows/api-tests.yml/badge.svg)
![Tests & Build UI](https://github.com/DevOpsQuizz/DevOps/actions/workflows/ui-test.yml/badge.svg)

## Architecture Générale
```graphql
DevOps/
 ├── .github/
 │     └── workflows/
 │           ├── api-tests.yml        # CI : tests Postman exécutés via Newman
 │           └── ui-test.yml          # CI : build / tests UI
 │
 ├── quiz-app/
 │     ├── quiz-api/                  # Backend Flask (Python)
 │     │     ├── app.py               # Entrée de l'application Flask
 │     │     ├── routes/              # Endpoints (auth, questions, =participations, leaderboard)
 │     │     ├── services/            # Logique métier
 │     │     ├── models.py            # Modèles SQLAlchemy
 │     │     ├── db.py                # Gestion SQLite
 │     │     ├── jwt_utils.py         # Utilitaires JWT
 │     │     ├── requirements.txt     # Dépendances Python
 │     │     └── Dockerfile           # Image Docker API (Gunicorn)
 │     │
 │     └── quiz-ui/                   # Frontend Vue 3 + Vite + Tailwind
 │           ├── src/
 │           │     ├── services/      # Requêtes API
 │           │     └── views/         # Composants/pages
 │           ├── package.json         # Dépendances NPM
 │           ├── nginx.conf           # Config Nginx pour la prod
 │           └── Dockerfile           # Build UI + serveur Nginx
 │
 └── README.md                        # Documentation du projet
```

Flux global:
1. L’API Flask écoute sur `http://127.0.0.1:5000` et sert les endpoints d’authentification et quiz.
2. Le frontend Vue consomme ces endpoints via `src/services/*`.
3. Les workflows CI valident que l’API répond correctement (via Postman) et que l’UI build/test passe.

## Prérequis

- Windows (PowerShell 5.1), ou WSL/Linux/Mac.
- Python 3.11+ (idéalement 3.12/3.13), `pip`.
- Node.js 20+ (ou 22), `npm`.
- Docker (optionnel, pour exécuter via containers).

## Lancer en Local (sans Docker)

1) Installer dépendances API

```powershell
# Depuis le dossier racine du repo
Set-Location "DevOps\quiz-app\quiz-api";
python -m venv venv; .\venv\Scripts\Activate.ps1;
pip install -r requirements.txt
```

2) Démarrer l’API Flask

```powershell
# Toujours dans quiz-api
python app.py
# L’API écoute sur http://127.0.0.1:5000
```

3) Installer dépendances UI

```powershell
Set-Location "DevOps\quiz-app\quiz-ui";
npm install
```

4) Démarrer le frontend (Vite dev server)

```powershell
npm run dev
# Ouvrir l’URL affichée
```

Note: Assurez-vous que l’UI cible bien `http://127.0.0.1:5000` pour l’API (variable ou constante `baseUrl` dans `src/services/*`).

## Lancer avec Docker

1) API en Docker

```powershell
Set-Location "DevOps\quiz-app\quiz-api";
docker build -t quiz-api:local .;
docker run -d -p 5000:5000 --name quiz-api-local quiz-api:local
# Vérifier: http://127.0.0.1:5000
```

2) UI en Docker (dev simple)

```powershell
Set-Location "DevOps\quiz-app\quiz-ui";
docker build -t quiz-ui:local -f Dockerfile .;
docker run -d -p 5173:5173 --name quiz-ui-local quiz-ui:local
# Ouvrir: http://localhost:5173
```

Arrêt des containers:

```powershell
docker rm -f quiz-api-local; docker rm -f quiz-ui-local; docker rm -f quiz-ui-prod
```

## Tests API (Postman/Newman)

- Collection: `quiz-app/quiz-ui/tests/test_postman_collection.json`.
- En CI, les tests utilisent `BASE_URL=http://127.0.0.1:5000` et un secret `ADMIN_PASSWORD`.

## Déploiement

```powershell
    # TODO
```

## Structure des Dossiers

```
quiz-app/
  quiz-api/        # Flask API (routes, services, models) + Dockerfile
  quiz-ui/         # Vue 3 + Vite + Tailwind + Dockerfiles
.github/workflows/ # CI pipelines (API tests, UI build/test)
```

## Astuces & Dépannage

- Port API: par défaut `5000`. Changer le mapping si déjà occupé (ex: `-p 5001:5000`).
- Node/Python versions: la CI teste plusieurs versions; alignez localement si possible.
- Logs Docker: `docker logs <container>` pour diagnostiquer.

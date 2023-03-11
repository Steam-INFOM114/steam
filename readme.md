# Projet STEAM

## Description
TODO

## Fonctionnalités
TODO

## How-to
### Développement
1. Installer docker
2. Depuis le répértoire où se trouve le fichier `docker-compose.dev.yml` exécuter la commande:
```bash
docker compose -f docker-compose.dev.yml up --build -d
```
3. Exécuter la commande:
```bash
docker exec django_dev python manage.py migrate
```
* le serveur de développement de django tourne sur: `127.0.0.1:8000`

### Déploiement

## Bugs et limitations
void

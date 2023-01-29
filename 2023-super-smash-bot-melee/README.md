# 2023 Simu project : Super Smash Bot Meele

## Règles du challenge

* Le terrain est une plateforme en hauteur
* Le but du challenge est de ne pas se faire ejecter ou de tomber de la plateforme
* Tous les coups sont permis
* Ejecter un robot adverse est recommandé pour avoir sa place sur le Podium
* Les robots ayant une attitude complètement passive (sans déplacement) seront EXCLUS
* Les robots restants sur la plateforme après un temps MAX de 5min seront VAINCEURS

## Installation

Exécuter le script suivant pour avoir la complétion des biblioth_qèes `Webots` dans `VS Code`

```bash
cd seatech-python-object-and-robotic-exo/02-webots
./setup_webots_environment.sh
```

## Règles de structuration

* le controller Webtos doit impérativement avoir le nom `my_controller`
* le dépôt Github doit contenir un UNIQUE projet webots (controllers, worlds, protos, ...)


## Utilisation du superviseur

`fetch_challengers_repositories.py` 
* clonera ou mettra à jour les dépôts des challengers dans le répertoire `challengers`
* copiera les répertoires 'my_controller' trouvés dans la simulation du superviseur dans le répertoire `controllers`

`seatech_battle_supervisor.py`
* récupérera la liste des challengers 

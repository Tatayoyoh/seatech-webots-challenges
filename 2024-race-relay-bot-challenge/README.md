# 2024 Simu project : Race Relay Bot Challenge

## Règles du challenge

* Le terrain se décompose en plusieurs types de terrains
* Chaque terrain est composé d'un challenge à résoudre
* Le challenge confrontera 4 équipes de 5 personnes
* Le but d'une équipe est de résoudre au plus vite les différents terrains : partir d'un point A pour arriver à un point B
* L'équipe gagante sera l'équipe qui réussira à résoudre les différents terrains le plus vite possible

Les terrains sont décomposés en trois types :
* suivit d'une route
* résolution d'orientation terreste
* résolution d'orentation aérienne

## Équipes

* **RevenuPassifRacing** : Pineau, Deleplanque, Fonbonne, Albouy, Poree
* **RCocobot** : Philippeau, Mialon, Faulque, Jacob, Fortunati
* **L'équipe 3** : Bulte, Besnard, Olanda, Lafont, Porte
* **L'équipe 7** : De cock, Arneodo, Pignol, Orlando, Mouhtadi

## Récupérer les projet

Le script suivant récupère les dépôts présents dans le fichier `repo-list`
```
python3 fetch_teams_repositories.py
```

## Lancer la simulation

Ouvrir `webots` (version 2023b), et ouvrir le monde présent dans `2024-race-relay-bot-challenge/worlds/2024-simu_project.wbt`

Démarer la simulation avec le bouton 'play'

Lancer ensuite le script du superviseur pour démarrer la simulation d'un équipe :
```
cd controllers/race_supervisor/
python3 race_supervisor.py
```
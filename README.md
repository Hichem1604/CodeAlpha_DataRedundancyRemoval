# CodeAlpha_DataRedundancyRemoval

Système de suppression de la redondance des données (Tâche 1, stage Cloud Computing CodeAlpha).

## Objectif
Vérifier chaque nouvelle donnée avant de l'ajouter à la base, la classer
(nouvelle, redondante ou faux positif) et n'insérer que les entrées uniques et vérifiées.

## Flux du système
Nouvelle donnée -> normalisation -> hachage -> comparaison avec la base
-> classification -> insertion ou rejet (avec la raison)

## Technologies
Python, SQLite (puis base cloud), hashlib, pytest

## Statut
En cours de développement.
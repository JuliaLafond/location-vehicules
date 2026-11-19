# Location de véhicules

Application console en Python pour gérer une agence de location de voitures et de motos.

## Participants

- Lafond Julia Bénédicte
- Wilfonde Succeda

## Lancer le programme

1. Installer Python 3.
2. Cloner le dépôt : git clone https://github.com/JuliaLafond/location-vehicules
3. Lancer : python mini_projet.py

Au démarrage, le programme charge agence.json. S'il n'existe pas, il démarre avec une agence vide.

## Données de démonstration

Pour tester avec des données prêtes à l'emploi, copier donnees_demo.json vers agence.json :

- Windows : copy donnees_demo.json agence.json
- Linux / macOS : cp donnees_demo.json agence.json

## Fonctionnalités

- Gestion des clients et des véhicules (voitures et motos)
- Réservation, annulation, départ et retour
- Maintenance des véhicules
- Recherche de véhicules disponibles (type, marque, tarif maximum)
- Tri des véhicules par tarif ou par marque
- Indicateurs : réservations par statut, revenus, locations par véhicule, véhicule le plus loué, retards
- Historique des opérations, conservé dans le JSON et consultable depuis le menu
- Sauvegarde automatique dans agence.json après chaque modification

## Règles de gestion

- Pas de chevauchement de réservations pour un même véhicule.
- Pas de location pendant une maintenance.
- Période [début, fin) : le nombre de jours est (fin - début).
- Voiture : (tarif + 5) par jour (assurance).
- Moto : tarif par jour, remise de 10 % au-delà de 3 jours.
- Retard : jours de retard × tarif × 2, ajoutés au total.
- Retour anticipé : recalcul sur les jours réellement utilisés (minimum 1 jour).
- Annulation possible uniquement si la réservation est confirmée : remboursement total si au moins 2 jours avant le début, sinon aucun.
- Un fichier JSON invalide n'est jamais écrasé : le programme s'arrête avec un message.

Tableau de bord des Médailles Olympiques

Ce projet a pour objectif de collecter, structurer et visualiser les données des médailles olympiques par pays et par discipline à partir du site [olympics-statistics.com](https://olympics-statistics.com).

Lancement des scripts Python

a) Scraper les pays et leurs médailles

Sur le terminal faire cette commande :

python scrape_pays.py


 b) Scraper les disciplines et les médailles par pays

Sur le terminal faire cette commande :

python scrape_sports_medals_by_country.py


c) Scraper les athlètes

Sur le terminal faire cette commande :
python scrape.athletes.py


2. Lancer le Dashboard (visualisations)

Lancer un live server   Mini Rapport de projet — Jeux Olympiques : Extraction, Nettoyage et Visualisation des données

Objectif du projet

L'objectif de ce projet est de collecter, nettoyer, structurer et visualiser*des données sur les Jeux Olympiques à partir du site web [https://olympics-statistics.com](https://olympics-statistics.com). Les données concernent :
- Les athlètes et leurs palmarès
- Les pays et le nombre de médailles gagnées
- Les sports et la répartition des médailles par pays

 Étapes du processus d'extraction

1. Collecte des données

a. Athlètes et palmarès (scrape_athletes.py)
- Le script explore l'alphabet (`a` à `z` + `special`) pour trouver tous les athlètes disponibles.
- Pour chaque athlète, le script récupère :
  - Prénom, nom
  - Pays représenté
  - Liste des médailles : type (or, argent, bronze), sport, discipline, ville
- Le tout est stocké dans `athletes_all.json`

Exemple :
json
{
  "first_name": "Usain",
  "last_name": "Bolt",
  "country": "Jamaica",
  "palmares": [
    {
      "medal": "or",
      "sport": "Athletics",
      "event": "100m",
      "city": "Beijing"
    }
  ]
}

 b. Pays et médailles (scrape_pays_online.py)
- Le script visite la page `/nations` et collecte tous les liens vers les profils pays.
- Pour chaque pays, il extrait les quantités de médailles .
- Résultat enregistré dans ‘donnees_pays_medailes.json’.

Exemple :
json
{
  "pays": "France",
  "or": 25,
  "argent": 17,
  "bronze": 12
}

c. Sports et répartition par pays (export_medals.py)
- Le script visite la page `/olympic-sports` pour trouver tous les sports.
- Pour chaque sport, il récupère la répartition des médailles par pays.
- Export dans `sports_medals_by_country.json`.

Exemple :
json
{
  "discipline": "Judo",
  "medailles": [
    {
      "pays": "Japon",
      "gold": 9,
      "silver": 2,
      "bronze": 1
    }
  ]
}
`
 Étapes de nettoyage et transformation

- Uniformisation des noms de pays (`country` → `pays`)
- Regroupement des médailles par type
- Suppression des valeurs vides ou nulles
- Réduction des noms longs et normalisation des disciplines sportives
- Fusion de certaines entrées redondantes

Fichier nettoyé pour la visualisation `Highcharts` :
json
{
  "name": "USA",
  "code": "US",
  "gold": 39,
  "silver": 41,
  "bronze": 33,
  "value": 113
}

Visualisation des données

Une page unique `dashboard.html` regroupe les 3 visualisations interactives :

1. Carte mondiale des médailles 
- Couleurs selon le nombre total de médailles par pays
- Tooltip avec détails 

2. Top 10 des pays les plus médaillés 
- Calcul dynamique des totaux
- Affichage clair et coloré

3.  Médailles par sport 
- Sélecteur de sport dynamique
- Affiche les parts de médailles pour chaque pays
   Mohamed Amir El hajoui El jaafari M1 DE

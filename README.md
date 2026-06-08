# Ymmo - Site de vente de biens immobilier

[![Python](https://img.shields.io/badge/Python-3.12-brightgreen.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-26.0-blue.svg)](https://www.docker.com/)
[![Zabbix](https://img.shields.io/badge/Zabbix-7.0-red.svg)](https://www.zabbix.com/)


## Table des matières

- [Présentation du projet](#-presentation-du-projet)
- [Installation et initialisation locale](#-installation-et-initialisation-locale)
- [Fonctionnalités clés](#-fonctionnalités-clés)
- [Architecture du projet](#-architecture-du-projet)
- [Analyse de données](#-analyse-de-données)

## Présentation du projet

**YMMO** est un groupe immobilier français spécialisé dans la vente et l'achat de biens immobiliers résidentiels et professionnels. Le projet vise à déployer une **infrastructure IT centralisée, sécurisée et scalable** permettant de gérer les opérations immobilières et d'interconnecter le siège d'Aix-en-Provence avec ses 12 agences réparties sur le territoire national.

## Installation et initialisation locale
1. Environnement et dépendances

```bash
# Clonage et activation du venv
git clone https://github.com/Smith06S/Projet-Fil-Rouge-B2.git
cd Projet-Fil-Rouge-B2
python -m venv venv
.\venv\Scripts\activate

# Installation forcée des librairies requises
pip install --force-reinstall flask psycopg2-binary bcrypt folium requests werkzeug
```

2. Configuration temporaire PostgreSQL (pg_hba.conf)

Modifier le fichier pg_hba.conf local pour passer les lignes IPv4 et IPv6 en mode trust :
```bash
host    all             all             127.0.0.1/32            trust
host    all             all             ::1/128                 trust
```

Redémarrer le service de base de données depuis le panneau des Services Windows.

3. Création et Restauration du fichier SQL

```bash
# Connexion à la base système pour créer la structure vide
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -h localhost -p 5432 -d postgres -c "CREATE DATABASE ymmo;"

# Importation du fichier d'initialisation de données
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -h localhost -p 5432 -d ymmo -f ymmo.sql
```

Note : Rebasculer ensuite le fichier pg_hba.conf en scram-sha-256 et mettre à jour le mot de passe utilisateur vers ymmo123 pour valider la conformité avec la configuration du script database.py.

4. Lancement de l'application

```bash
python app.py
```
---

## Fonctionnalités clés

* **Espace Client :**
    * Sélection de l'agence locale à l'entrée.
    * Moteur de recherche multicritères avancé (budget, surface, type de bien, chauffage, balcon, parking, ascenseur).
    * Système de gestion des favoris par compte.
    * Messagerie privée avec les commerciaux en tâche de fond (polling automatique rafraîchi toutes les 3 secondes).
* **Espace Commercial :**
    * CRUD complet sur les annonces immobilières (avec gestion du téléversement d'images).
    * Isolation stricte des données : interdiction de modifier ou supprimer un bien d'une autre agence.
    * Gestion des messages et suivi clients.
* **Espace Administrateur :**
    * Création et affectation des comptes commerciaux avec génération automatique de matricule unique (`MAT-XXXX`).
    * Audit global et modération absolue (suppression en cascade des comptes via l'adresse email).

---

## Architecture du projet

Le code applique les principes **SOLID, DRY et KISS** à travers un pattern **MVC / Repository** :

```text
Projet-Fil-Rouge-B2/
├── app.py                      # Point d'entrée de l'application Flask
├── database.py                 # Gestion du pool de connexions PostgreSQL
├── controllers/                # Logique applicative et routage HTTP
│   ├── agence_controller.py
│   ├── auth_controller.py
│   ├── bien_controller.py
│   ├── chat_controller.py
│   └── dashboard_controller.py
├── models/                     # Entités POO, requêtes SQL et couches Repository
│   ├── agence.py
│   ├── bien.py
│   ├── carte.py                # Géocodage API Adresse et rendu cartographique Folium
│   ├── messagerie.py
│   └── utilisateur.py          # Hachage et salage sécurisé des mots de passe (Bcrypt)
├── helpers/                    # Middleware et gestion d'accès RBAC (auth_helper.py)
├── static/                     # CSS responsive, images et téléversements d'annonces
└── templates/                  # Vues HTML5 gérées via le moteur Jinja2
```
---

## Analyse de données

Calculs et indicateurs métiers générés en temps réel via des fonctions d'agrégation SQL et traitement Python :

- Prix moyen au m² calculé dynamiquement par secteur géographique.

- Indice de popularité des logements selon le volume de mises en favoris.

- Algorithme prédictif pondéré pour l'évolution des prix sur le marché.

- Estimation statistique du volume de ventes annuelles par zone.

**Développé par l'équipe Ymmo**

*Dernière mise à jour : Juin 2026* 
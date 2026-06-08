# Proposition de Solution Cloud - YMMO Immobilier

## Objectif

Présenter une proposition de solution cloud AWS pour YMMO, en définissant les composantes techniques principales et la manière dont elles s’intègrent à l’infrastructure existante.

## Architecture cible

- **Modèle hybride** : siège local + extensions cloud pour les agences
- **Réseau** : VPC AWS privé connecté au siège via un tunnel VPN chiffré
- **Annuaire** : Active Directory principal conservé au siège, avec lien contrôlé vers AWS
- **Données critiques** : conservées en local, les données non sensibles peuvent être dupliquées ou sauvegardées dans le cloud

## Ce qui reste au siège
- Domaine Active Directory principal
- Base de données centrale
- Services critiques de production
- Gestion des utilisateurs et des accès principaux

## Ce qu’AWS apporte
- Accroître l’agilité des agences sans déplacer le cœur du système
- Héberger des fonctions applicatives légères en cloud
- Fournir un point de sauvegarde externe sécurisé
- Décharger une partie du trafic et de la maintenance locale

## Services AWS recommandés par fonction

- **AWS VPC** : réseau isolé avec sous-réseaux pour les ressources agences, routage vers le siège
- **EC2** : instances pour héberger les applications agences et les services web légers
- **AWS Directory Service** : point de jonction avec l’AD local, permettant l’accès contrôlé aux ressources cloud
- **AWS Site-to-Site VPN** : tunnel IPSec entre le siège et AWS pour relier le réseau local et le VPC
- **Amazon S3** : stockage d’objets chiffrés pour sauvegardes, fichiers de logs et archives
- **CloudWatch** : supervision des ressources cloud, collecte de métriques et alertes basiques

## Positionnement technique

- Le cloud n’est pas ici un remplacement du siège, mais un prolongement
- AWS sert à accueillir des ressources secondaires et des sauvegardes
- La solution doit rester simple, avec un minimum de services nécessaires
- L’architecture hybride garantit que les fonctions critiques restent sous contrôle local

## Proposition de solution

Utiliser AWS comme complément de l’infrastructure YMMO en conservant :
- le SIège comme base primaire,
- le cloud comme environnement d’extension,
- l’AD locale pour l’authentification principale,
- S3 pour les sauvegardes et archives non sensibles.

---


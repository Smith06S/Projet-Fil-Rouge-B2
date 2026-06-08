# CAHIER DES CHARGES TECHNIQUE - INFRASTRUCTURE YMMO

**Projet :** Infrastructure réseau et système d'information  
**Client :** YMMO - Groupe immobilier  
**Date :** Février 2026  
**Version :** 1.0

---

## 1. PRÉSENTATION DU PROJET

### 1.1 Contexte
YMMO est un groupe immobilier français spécialisé dans la vente et l'achat de biens immobiliers résidentiels et professionnels. L'entreprise dispose d'un siège à Aix-en-Provence et d'un réseau de 12 agences réparties sur le territoire national.

### 1.2 Problématique
L'entreprise souhaite mettre en place une infrastructure réseau centralisée et sécurisée permettant de :
- Centraliser la gestion des utilisateurs et des ressources
- Interconnecter le siège et les 12 agences
- Garantir la sécurité des données et des accès
- Faciliter le travail collaboratif entre les sites
- Superviser l'ensemble de l'infrastructure

### 1.3 Objectifs du projet
- Déployer une infrastructure Active Directory pour la gestion centralisée
- Mettre en place une solution web pour la gestion immobilière
- Interconnecter tous les sites via VPN IPSec site-à-site
- Implémenter une politique de sécurité robuste
- Assurer la supervision et le monitoring de l'infrastructure

---

## 2. ARCHITECTURE TECHNIQUE

*L'architecture réseau détaillée est documentée dans :*
- **Plan d'adressage IP :** Voir [plan-adressage-ip.md](plan-adressage-ip.md)
- **Spécifications techniques :** Voir [specifications-techniques.md](specifications-techniques.md)

### 2.1 Vue d'ensemble

**Siège Aix-en-Provence (10.0.0.0/24) :** 30 utilisateurs + 4 serveurs
**12 Agences (10.1.0.0/24 à 10.12.0.0/24) :** 5 commerciaux par agence
**Interconnexion :** VPN IPSec site-à-site (12 tunnels)
**Réseau VPN Management :** 172.16.0.0/24

### 2.2 Équipements critiques

---

## 3. SERVICES DÉPLOYÉS

*Les services détaillés sont documentés dans les fichiers suivants :*
- **Configuration détaillée :** Voir [liste-services-deployer.md](liste-services-deployer.md)
- **Spécifications techniques :** Voir [specifications-techniques.md](specifications-techniques.md)
- **Guide de configuration :** Voir [guide-configuration-serveurs.md](guide-configuration-serveurs.md)

### 3.1 Résumé des services

**DC-SIEGE (10.0.0.10) :** Active Directory, DNS, DHCP, Partages réseau
**SRV-WEB-BDD (10.0.0.11) :** Apache Web Server, Python 3.x / Flask, MySQL 8.0, Samba
**SRV-DOCKER-MONITORING (10.0.0.12) :** Dockge, Traefik, Uptime Kuma, Zabbix
**Firewall (10.0.0.1) :** OPNSense (Stateful Firewall, VPN IPSec, NAT/PAT, IDS/IPS)
**NAS (10.0.0.20) :** Synology DS920+ (Sauvegarde, RAID 5)

---

## 4. POLITIQUE DE SÉCURITÉ

*La politique de sécurité détaillée est documentée dans :*
- **Document complet :** Voir [politique-securite.md](politique-securite.md)
- **Matrice des droits :** Voir [matrice-droits-acces.md](matrice-droits-acces.md)

### 4.1 Principes de sécurité

- **Moindre privilège :** Accès restreint au strict nécessaire
- **Défense en profondeur :** Plusieurs couches de sécurité
- **Traçabilité complète :** Journalisation de tous les accès
- **Chiffrement des données :** En transit (TLS, IPSec) et au repos
- **Authentification forte :** MFA pour accès administratifs

---

## 5. PLAN DE DÉPLOIEMENT

### 5.1 Phase 1 - Préparation (Semaine 1)
- Installation de l'infrastructure matérielle au siège
- Configuration du réseau et de l'adressage IP
- Installation des serveurs physiques
- Configuration du firewall principal

### 5.2 Phase 2 - Services de base (Semaine 2)
- Déploiement Active Directory
- Configuration DNS et DHCP
- Création de la structure organisationnelle
- Création des utilisateurs et groupes

### 5.3 Phase 3 - Services applicatifs (Semaine 3)
- Installation et configuration du serveur Web
- Déploiement de la base de données
- Configuration des partages de fichiers
- Déploiement des services Docker

### 5.4 Phase 4 - Interconnexion (Semaine 4)
- Configuration des firewalls d'agence
- Établissement des tunnels VPN IPSec
- Tests de connectivité inter-sites
- Intégration des postes d'agence au domaine

### 5.5 Phase 5 - Sécurisation et monitoring (Semaine 5)
- Application des GPO de sécurité
- Configuration du monitoring
- Tests de sécurité et audit
- Formation des utilisateurs

### 5.6 Phase 6 - Production et support (Semaine 6)
- Mise en production
- Documentation finale
- Transfert de compétences
- Support post-déploiement

---

## 6. CONTRAINTES ET EXIGENCES

### 6.1 Contraintes techniques
- Compatibilité avec l'existant (postes Windows 10/11)
- Bande passante minimum : 100 Mbps au siège, 50 Mbps en agence
- Disponibilité cible : 99.5% (temps d'arrêt max 3.6h/mois)
- Temps de réponse maximum : 200ms entre siège et agences

### 6.2 Contraintes réglementaires
- Conformité RGPD (protection des données personnelles)
- Conservation des logs pendant 12 mois minimum
- Chiffrement des données sensibles
- Politique de sauvegarde conforme aux normes métier

### 6.3 Contraintes budgétaires
- Budget initial : 90 000 - 100 000 €
- Budget annuel récurrent : ~17 000 €/an
- ROI attendu : 3 ans

---

## 7. LIVRABLES

### 7.1 Documentation technique
- Schéma d'architecture réseau complet
- Plan d'adressage IP détaillé
- Guide de configuration des serveurs
- Politique de sécurité
- Plan de gestion des droits d'accès
- Procédures de sauvegarde et restauration
- Guide d'exploitation et de maintenance

### 7.2 Infrastructure
- 3 serveurs configurés et opérationnels
- 1 NAS configuré
- Active Directory fonctionnel avec 90 utilisateurs
- 12 tunnels VPN opérationnels
- Application web accessible
- Monitoring en place sur tous les services

### 7.3 Formation
- Formation administrateurs IT (2 jours)
- Formation utilisateurs finaux (1 jour)
- Documentation utilisateur

---

## 8. INDICATEURS DE SUCCÈS

- ✅ 100% des utilisateurs peuvent se connecter au domaine
- ✅ 100% des agences sont connectées via VPN
- ✅ Disponibilité des services > 99.5%
- ✅ Temps de réponse < 200ms inter-sites
- ✅ 0 incident de sécurité majeur
- ✅ Sauvegardes quotidiennes réussies à 100%
- ✅ Satisfaction utilisateurs > 80%

---

## 9. GLOSSAIRE

- **AD :** Active Directory
- **DHCP :** Dynamic Host Configuration Protocol
- **DNS :** Domain Name System
- **GPO :** Group Policy Object (Stratégie de groupe)
- **IDS/IPS :** Intrusion Detection/Prevention System
- **IPSec :** Internet Protocol Security
- **NAS :** Network Attached Storage
- **NAT :** Network Address Translation
- **OU :** Organizational Unit (Unité organisationnelle)
- **RAID :** Redundant Array of Independent Disks
- **VPN :** Virtual Private Network

---

**Document validé par :**
- Chef de projet INFRA : [Nom]
- Client YMMO : [Nom]
- Date de validation : [Date]

**Version :** 1.0  
**Date de dernière mise à jour :** Février 2026

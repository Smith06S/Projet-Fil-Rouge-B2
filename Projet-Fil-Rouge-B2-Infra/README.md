# Documentation Technique - Projet YMMO Immobilier

[![Python](https://img.shields.io/badge/Python-3.12-brightgreen.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-26.0-blue.svg)](https://www.docker.com/)
[![Zabbix](https://img.shields.io/badge/Zabbix-7.0-red.svg)](https://www.zabbix.com/)

## Table des matières

- [Présentation du projet](#-presentation-du-projet)
- [Objectifs clés](#-ojectifs-clés)
- [Vue d'ensemble de l'infrastructure](#-vue-d'ensemble-de-l'infrastructure)
- [Principes clés de sécurité](#-principe-clés-de-sécurité)
- [Métriques cibles](#-métrique-cibles)
- [Guide de démarrage](#-guide-de-démarrage)
- [Budget et ressources](#-budget-et-ressources)
- [Contacts et support](#-contacts-et-support)
- [Notes importantes](#-notes-importantes)

## 📖 Présentation du projet

**YMMO** est un groupe immobilier français spécialisé dans la vente et l'achat de biens immobiliers résidentiels et professionnels. Le projet vise à déployer une **infrastructure IT centralisée, sécurisée et scalable** permettant de gérer les opérations immobilières et d'interconnecter le siège d'Aix-en-Provence avec ses 12 agences réparties sur le territoire national.

### 🎯 Objectifs clés
- ✅ Active Directory centralisé pour gestion des utilisateurs et ressources
- ✅ Application web de gestion immobilière
- ✅ Interconnexion sécurisée (VPN IPSec) de tous les sites
- ✅ Politique de sécurité robuste et conformité RGPD
- ✅ Supervision et monitoring complets de l'infrastructure
- ✅ Plan de sauvegarde et continuité de service

---

## 📚 Index de la documentation

### 1. **[cahier-charges-technique-infra.md](Markdowns/cahier-charges-technique-infra.md)** 📋
**Document principal du projet**

Contient le cahier des charges complet avec :
- Contexte et problématique du projet YMMO
- Architecture technique globale (topologie réseau, serveurs, interconnexion)
- Vue résumée des services déployés
- Principes de sécurité et sauvegarde
- Plan de déploiement en 6 phases
- Indicateurs de succès et livrables attendus
- Budget et contraintes

💡 *À lire en premier pour comprendre l'ensemble du projet*

---

### 2. **[plan-adressage-ip.md](Markdowns/plan-adressage-ip.md)** 🌐
**Plan réseau complet et exhaustif**

Contient le détail de chaque adresse IP :
- Réseau siège (10.0.0.0/24) : 254 adresses avec réservations
- Réseaux des 12 agences (10.1.0.0/24 à 10.12.0.0/24)
- Réseau VPN Management (172.16.0.0/24)
- Enregistrements DNS principaux
- Conventions de nommage pour tous les équipements
- Règles de gestion et de modification

💡 *Référence pour toute question d'adressage IP*

---

### 3. **[liste-services-deployer.md](Markdowns/liste-services-deployer.md)** 🔧
**Inventaire détaillé de tous les services**

Énumère les 18 services à déployer


---

### 4. **[guide-configuration-serveurs.md](Markdowns/guide-configuration-serveurs.md)** 🛠️
**Guide pratique d'installation et configuration**

Procédures pas-à-pas pour configurer :
- Contrôleur de domaine Active Directory
- Serveur Web et Base de données (Apache + MySQL)
- Serveur Docker et services de monitoring
- Firewall OPNSense
- Checklist de vérification post-déploiement
- Troubleshooting des problèmes courants

💡 *À utiliser pendant l'installation et la configuration*

---

### 5. **[guide-deploiement.md](Markdowns/guide-deploiement.md)** 🚀
**Plan de déploiement détaillé et checklists**

Contient :
- Prérequis matériels et logiciels
- Architecture VMware pour le laboratoire
- Spécifications de chaque VM
- Checklist complète de déploiement par phase
- Scripts d'automatisation PowerShell et Bash
- Tests de validation et troubleshooting
- Timeline de mise en production

💡 *Guide d'exécution du déploiement au jour le jour*

---

### 6. **[specifications-techniques.md](Markdowns/specifications-techniques.md)** ⚙️
**Spécifications techniques exhaustives**

Document de référence contenant :
- Vue d'ensemble et objectifs techniques
- Architecture réseau détaillée avec tables d'adressage
- Spécifications matériques de chaque serveur (CPU, RAM, stockage)
- Configuration logicielle complète (OS, services, versions)
- Stack applicative web (Frontend, Backend, BD)
- Règles de sécurité réseau et firewall
- Configuration VPN IPSec détaillée
- Performance et dimensionnement estimé

💡 *Référence pour tous les détails techniques*

---

### 7. **[politique-securite.md](Markdowns/politique-securite.md)** 🔒
**Politique de sécurité informatique complète**

Couvre tous les aspects de sécurité :
- Gestion des mots de passe et authentification (GPO)
- Authentification Multi-Facteurs (MFA)
- Sécurité réseau (firewall, VPN IPSec, accès WiFi)
- Hardening des serveurs Windows et Linux
- Gestion des accès administrateurs
- Patch Management et mises à jour
- Sauvegarde et récupération d'urgence
- Protection des données et conformité RGPD
- Détection et réponse aux incidents
- Utilisation acceptable des ressources IT

💡 *Référence pour la conformité et la sécurité*

---

### 8. **[matrice-droits-acces.md](Markdowns/matrice-droits-acces.md)** 👥
**Matrice complète des droits d'accès par rôle**

Détaille les permissions pour :
- 5 rôles principaux : Direction, Commercial, Marketing, RH-Juridique, IT-Support
- Partages réseau (Direction, Commercial, Marketing, RH, IT)
- Services Active Directory
- Application web YMMO (CRUD, transactions, exports)
- Outils de monitoring (Uptime Kuma, Zabbix, Dockge, Traefik)
- Infrastructure (serveurs, équipements réseau)
- Accès VPN et Tailscale
- Base de données MySQL
- Procédures d'audit et révision des droits
- Conformité RGPD

💡 *Référence pour la gestion des permissions et du moindre privilège*

---

### 9. **[plan-sauvegarde-supervision.md](Markdowns/plan-sauvegarde-supervision.md)** 💾
**Plan de sauvegarde, supervision et continuité**

Stratégie complète avec :
- Objectifs RPO (24h) et RTO (4h)
- Calendrier de sauvegarde (AD, MySQL, Application)
- Procédures de sauvegarde et restauration
- Outils de supervision (Uptime Kuma, Zabbix)
- Monitors configurés et métriques supervisées
- Alertes et seuils critiques
- Configuration des notifications
- Rapports périodiques (hebdo/mensuel)
- Maintenance préventive et corrective
- Escalade des incidents
- Métriques de performance (MTBF, MTTR, SLA)
- Plan de continuité et procédures de basculement

💡 *Référence pour la disponibilité et la supervision*

---

### 10. **[solution-cloud.md](Markdowns/solution-cloud.md)** ☁️
**Analyse comparative : On-Premise vs Cloud**

Propose une alternative cloud avec :
- Comparaison des architectures (On-Premise, Cloud, Hybride)
- Architecture Azure recommandée
- Détail des services Azure (VMs, App Service, SQL Database, Storage, Monitoring)
- Azure AD et authentification
- Options de déploiement (3 scénarios)
- Analyse financière sur 5 ans
- Plan de migration hybride (6 mois)
- Considérations de sécurité et RGPD
- Timeline et roadmap cloud

💡 *Pour explorer une évolution future vers le cloud*

---

## 📊 Vue d'ensemble de l'infrastructure

```
┌────────────────────────────────────────┐
│   Siège Aix-en-Provence (10.0.0.0/24)  │
│                                        │
│  DC-SIEGE (10.0.0.10)                  │
│  ├─ Active Directory (ymmo.local)      │
│  ├─ DNS Server                         │
│  └─ DHCP Server                        │
│                                        │
│  SRV-WEB-BDD (10.0.0.11)               │
│  ├─ Apache 2.4 + Python 3.x / Flask    │
│  ├─ MySQL 8.0                          │
│  └─ Samba                              │
│                                        │
│  SRV-DOCKER (10.0.0.12)                │
│  ├─ Dockge (orchestration)             │
│  ├─ Traefik (reverse proxy)            │
│  ├─ Uptime Kuma (monitoring)           │
│  └─ Zabbix (supervision)               │
│                                        │
│  NAS-BACKUP (10.0.0.20)                │
│  └─ Synology RAID 5 (12 TB)            │
│                                        │
│  FW-SIEGE (10.0.0.1)                   │
│  └─ OPNSense Firewall + VPN IPSec      │
└────────────────────────────────────────┘
           │
           │ VPN IPSec (12 tunnels)
           │ 10.0.0.0/24 ↔ 10.x.0.0/24
           ▼
┌────────────────────────────────────────┐
│   12 Agences (Paris, Lyon, Marseille...) │
│   Chacune : 10.x.0.0/24                │
│   - OPNSense Firewall                  │
│   - 5 Postes commerciaux               │
│   - Imprimante réseau                  │
└────────────────────────────────────────┘
```

---

## 🔐 Principes clés de sécurité

- **Authentification** : Active Directory centralisé + MFA pour accès administratifs
- **Firewall** : OPNSense avec politique "DENY ALL" par défaut
- **VPN** : IPSec IKEv2 + AES-256-GCM entre tous les sites
- **Mots de passe** : Minimum 8 caractères, complexité, renouvellement 90 jours
- **Sauvegarde** : RPO 24h, RTO 4h, rétention 30 jours minimum
- **Compliance** : RGPD, conformité logs, audit trimestriel des droits

---

## 📈 Métriques cibles

| Métrique | Objectif |
|----------|----------|
| **Disponibilité** | 99.5% (3.6h downtime/mois) |
| **Temps de réponse** | < 200ms inter-sites |
| **RPO (Backup)** | 24 heures |
| **RTO (Récupération)** | 4 heures |
| **Satisfaction utilisateurs** | > 80% |
| **Zéro incident sécurité** | Cible |

---

## 🚀 Guide de démarrage

1. **Comprendre le projet** → Lire [cahier-charges-technique-infra.md](Markdowns/cahier-charges-technique-infra.md)
2. **Vérifier l'adressage** → Consulter [plan-adressage-ip.md](Markdowns/plan-adressage-ip.md)
3. **Planifier le déploiement** → Suivre [guide-deploiement.md](Markdowns/guide-deploiement.md)
4. **Configurer les serveurs** → Utiliser [guide-configuration-serveurs.md](Markdowns/guide-configuration-serveurs.md)
5. **Mettre en place la sécurité** → Appliquer [politique-securite.md](Markdowns/politique-securite.md)
6. **Configurer les droits** → Implémenter [matrice-droits-acces.md](Markdowns/matrice-droits-acces.md)
7. **Valider la supervision** → Vérifier [plan-sauvegarde-supervision.md](Markdowns/plan-sauvegarde-supervision.md)

---

## 💾 Budget et ressources

- **Budget initial** : 90 000 - 100 000 €
- **Budget annuel** : ~17 000 € (maintenance, électricité, support)
- **ROI attendu** : 3 ans
- **Équipe requise** : 1-2 administrateurs IT full-time

---

## 📞 Contacts et support

- **IT Support** : it-support@ymmo.local
- **DPO (RGPD)** : dpo@ymmo.local
- **Sécurité** : security@ymmo.local
- **Direction** : direction@ymmo.local

---

## 📝 Notes importantes

⚠️ **Ce projet est un laboratoire d'apprentissage (LAB)**
- Les mots de passe affichés sont des exemples uniquement
- Les PSK VPN doivent être générés aléatoirement en production
- Les certificats SSL doivent être signés par une CA en production
- L'architecture doit être validée par un consultant sécurité avant production

---

**Version** : 1.0  
**Dernière mise à jour** : Juin 2026  
**Statut** : En production LAB

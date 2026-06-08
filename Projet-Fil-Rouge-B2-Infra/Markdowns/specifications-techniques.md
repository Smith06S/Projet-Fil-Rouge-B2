# SPÉCIFICATIONS TECHNIQUES - INFRASTRUCTURE YMMO

**Projet :** Infrastructure réseau et système d'information YMMO  
**Version :** 1.0  
**Date :** Février 2026  
**Type :** Spécifications techniques détaillées

---

## SOMMAIRE

1. Vue d'ensemble du projet
2. Architecture réseau
3. Infrastructure serveurs
4. Services et applications
5. Sécurité
6. Sauvegarde et disponibilité
7. Performances et dimensionnement
8. Matériel et budget

---

## 1. VUE D'ENSEMBLE DU PROJET

### 1.1 Contexte et besoin

**Client :** YMMO - Groupe immobilier français  
**Implantation géographique :**
- 1 siège social à Aix-en-Provence
- 12 agences réparties sur le territoire national

**Besoin :**
Déployer une infrastructure IT centralisée, sécurisée et scalable permettant de gérer les opérations immobilières du groupe et d'interconnecter tous les sites.

### 1.2 Objectifs techniques

- ✅ Centralisation des identités et authentification (Active Directory)
- ✅ Application web de gestion immobilière
- ✅ Interconnexion sécurisée des 13 sites (VPN IPSec)
- ✅ Monitoring et supervision de l'infrastructure
- ✅ Politique de sécurité robuste (GPO, Firewall, Chiffrement)
- ✅ Plan de sauvegarde et de reprise d'activité

### 1.3 Contraintes

**Techniques :**
- Compatibilité avec postes Windows 10/11 existants
- Disponibilité cible : 99.5% (3.6h downtime/mois max)
- Temps de réponse inter-sites < 200ms
- Bande passante minimum : 100 Mbps siège, 50 Mbps agences

**Budgétaires :**
- Budget initial : 90 000 - 100 000 €
- Budget récurrent : ~17 000 €/an

**Réglementaires :**
- Conformité RGPD
- Conservation logs 12 mois minimum
- Chiffrement données sensibles

---

## 2. ARCHITECTURE RÉSEAU

### 2.1 Topologie générale

```
INTERNET
    │
    ├─── [Siège Aix-en-Provence]
    │    Réseau : 10.0.0.0/24
    │    Firewall : 10.0.0.1
    │    └─── VPN IPSec ←──┐
    │                       │
    ├─── [Agence Paris]     │
    │    Réseau : 10.1.0.0/24
    │    Firewall : 10.1.0.1 ──┘
    │    
    ├─── [Agence Lyon]
    │    Réseau : 10.2.0.0/24
    │    
    └─── [...10 autres agences]
         Réseaux : 10.3.0.0/24 à 10.12.0.0/24
```

### 2.2 Plan d'adressage IP détaillé

#### Siège Aix-en-Provence - 10.0.0.0/24

| Plage IP | Usage | Nombre |
|----------|-------|--------|
| 10.0.0.1 | Firewall OPNSense LAN | 1 |
| 10.0.0.2 | Switch Core | 1 |
| 10.0.0.10 | Serveur DC-SIEGE (AD/DNS/DHCP) | 1 |
| 10.0.0.11 | Serveur SRV-WEB-BDD (Apache/MySQL) | 1 |
| 10.0.0.12 | Serveur SRV-DOCKER-MONITORING | 1 |
| 10.0.0.20 | NAS Synology (Backup) | 1 |
| 10.0.0.50-99 | Réservé (extension future) | 50 |
| 10.0.0.100-130 | Pool DHCP postes de travail | 31 |
| 10.0.0.200 | Imprimante réseau | 1 |
| 10.0.0.254 | Interface VMnet2 (LAB uniquement) | 1 |

#### Agences - 10.x.0.0/24 (x = 1 à 12)

| Plage IP | Usage |
|----------|-------|
| 10.x.0.1 | Firewall OPNSense LAN |
| 10.x.0.2 | Switch 8 ports |
| 10.x.0.100-110 | Pool DHCP postes commerciaux (5 utilisés, 6 réservés) |
| 10.x.0.200 | Imprimante |

#### Réseau VPN Management - 172.16.0.0/24

| IP | Usage |
|----|-------|
| 172.16.0.1 | Endpoint VPN Siège |
| 172.16.0.10-21 | Endpoints VPN Agences (1-12) |

### 2.3 Configuration DHCP

**Serveur DHCP Siège :** DC-SIEGE (10.0.0.10)

**Étendue Siège :**
- Nom : "Réseau Siège Aix-en-Provence"
- Plage : 10.0.0.100 - 10.0.0.130
- Masque : 255.255.255.0 (/24)
- Passerelle : 10.0.0.1
- DNS : 10.0.0.10
- Domaine : ymmo.local
- Durée de bail : 8 jours

**Serveurs DHCP Agences :** OPNSense local (10.x.0.1)
- Plage : 10.x.0.100 - 10.x.0.110
- Passerelle : 10.x.0.1
- DNS : 10.0.0.10 (via VPN)
- Domaine : ymmo.local

### 2.4 Configuration DNS

**Serveur DNS principal :** DC-SIEGE (10.0.0.10)

**Zone : ymmo.local (Active Directory-integrated)**

| Nom | Type | Valeur | Description |
|-----|------|--------|-------------|
| @ | A | 10.0.0.10 | Domaine principal |
| dc-siege | A | 10.0.0.10 | Contrôleur de domaine |
| srv-web-bdd | A | 10.0.0.11 | Serveur web et BDD |
| srv-docker-monitoring | A | 10.0.0.12 | Serveur Docker |
| nas-backup | A | 10.0.0.20 | NAS sauvegarde |
| fw-siege | A | 10.0.0.1 | Firewall siège |
| www | CNAME | srv-web-bdd.ymmo.local | Alias web |
| monitoring | CNAME | srv-docker-monitoring.ymmo.local | Alias monitoring |
| _ldap._tcp | SRV | dc-siege.ymmo.local:389 | Service LDAP |
| _kerberos._tcp | SRV | dc-siege.ymmo.local:88 | Service Kerberos |

**Zone de recherche inversée :** 0.0.10.in-addr.arpa

**Redirecteurs (Forwarders) :**
- 8.8.8.8 (Google DNS)
- 1.1.1.1 (Cloudflare DNS)

---

## 3. INFRASTRUCTURE SERVEURS

### 3.1 Serveur 1 - DC-SIEGE (10.0.0.10)

#### Matériel (Production)
- **Modèle :** Dell PowerEdge R240 ou équivalent
- **CPU :** Intel Xeon E-2224 (4 cœurs @ 3.4 GHz)
- **RAM :** 16 GB DDR4 ECC
- **Stockage :** 2x 1TB SATA en RAID 1 (miroir)
- **Réseau :** 2x 1 Gbps (teaming recommandé)
- **Alimentation :** Redondante (2x PSU)

#### Système d'exploitation
- **OS :** Windows Server 2022 Standard (Desktop Experience)
- **Licence :** 2 licences processeur
- **CAL :** 90 licences utilisateurs
- **Niveau fonctionnel domaine :** Windows Server 2022

#### Rôles et services
1. **Active Directory Domain Services**
   - Domaine : ymmo.local
   - NetBIOS : YMMO
   - FSMO Roles : Tous (forêt à domaine unique)

2. **DNS Server**
   - Zone principale : ymmo.local
   - Zone inversée : 0.0.10.in-addr.arpa

3. **DHCP Server**
   - Étendue siège : 10.0.0.100-130

4. **File Services**
   - Partages : Direction, Commercial, Marketing, RH-Juridique, IT-Support

#### Performance et dimensionnement
- **RAM utilisée (estimation) :** 8-10 GB
- **CPU moyen :** < 30%
- **IOPS requis :** 500-1000 IOPS
- **Bande passante :** 100 Mbps pic

---

### 3.2 Serveur 2 - SRV-WEB-BDD (10.0.0.11)

#### Matériel (Production)
- **Modèle :** Dell PowerEdge R240 ou équivalent
- **CPU :** Intel Xeon E-2224 (4 cœurs @ 3.4 GHz)
- **RAM :** 32 GB DDR4 ECC
- **Stockage :** 2x 2TB SATA en RAID 1
- **Réseau :** 2x 1 Gbps (teaming recommandé)

#### Système d'exploitation
- **OS :** Ubuntu Server 22.04 LTS
- **Kernel :** 5.15 ou supérieur
- **Architecture :** x86_64

#### Stack applicative

**1. Apache HTTP Server 2.4**
- Port : 80 (HTTP), 443 (HTTPS)
- Document Root : /var/www/html/ymmo
- Virtual Host : ymmo.local, www.ymmo.local
- Modules : mod_rewrite, mod_ssl, mod_proxy, mod_proxy_http, mod_headers
- Max Workers : 150
- KeepAlive : On
- Timeout : 300s

**2. Python 3.x / Flask**
- Version : Python 3.10+ ou supérieur
- Framework : Flask
- Bibliothèques : flask, flask-cors, python-dotenv, mysqlclient
- Environnement : Virtualenv ou venv
- Entrypoint : /var/www/html/ymmo/app.py
- Exposition : Apache reverse proxy vers Flask ou service WSGI/Gunicorn

**3. MySQL 8.0 / MariaDB**
- Port : 3306
- Base : ymmo_db
- User : ymmo_user
- Charset : utf8mb4_unicode_ci
- Max connections : 150
- InnoDB buffer pool : 16 GB

**4. Samba 4.x**
- Partage : Documents-YMMO
- Path : /srv/samba/documents-ymmo
- Protocole : SMBv3 avec chiffrement

#### Performance et dimensionnement
- **RAM utilisée :** 20-24 GB
- **CPU moyen :** < 40%
- **IOPS requis :** 1000-2000 IOPS
- **Bande passante :** 200 Mbps pic
- **Connexions simultanées :** 50 utilisateurs

---

### 3.3 Serveur 3 - SRV-DOCKER-MONITORING (10.0.0.12)

#### Matériel (Production)
- **Modèle :** HP ProLiant DL20 Gen10 ou équivalent
- **CPU :** Intel Xeon E-2236 (6 cœurs @ 3.4 GHz)
- **RAM :** 16 GB DDR4 ECC
- **Stockage :** 1TB SSD NVMe
- **Réseau :** 2x 1 Gbps

#### Système d'exploitation
- **OS :** Ubuntu Server 22.04 LTS
- **Docker Engine :** 24.x ou supérieur
- **Docker Compose :** v2.20 ou supérieur

#### Conteneurs Docker

| Service | Image | Port(s) | RAM allouée | CPU |
|---------|-------|---------|-------------|-----|
| Dockge | louislam/dockge:1 | 5001 | 512 MB | 0.5 |
| Traefik | traefik:v2.11 | 80, 443, 8080 | 512 MB | 0.5 |
| Uptime Kuma | louislam/uptime-kuma:1 | 3001 | 512 MB | 0.25 |
| Zabbix Server | zabbix/zabbix-server-pgsql | - | 2 GB | 1 |
| Zabbix Web | zabbix/zabbix-web-nginx-pgsql | 8081 | 1 GB | 0.5 |
| PostgreSQL | postgres:15-alpine | 5432 | 2 GB | 1 |

#### Performance et dimensionnement
- **RAM utilisée :** 8-12 GB
- **CPU moyen :** < 30%
- **IOPS requis :** 500 IOPS (SSD)
- **Bande passante :** 50 Mbps

---

### 3.4 NAS - NAS-BACKUP (10.0.0.20)

#### Matériel
- **Modèle :** Synology DS920+ (4 baies)
- **Disques :** 4x 4TB WD Red Plus (NAS-grade)
- **RAID :** RAID 5 (capacité utile : ~12 TB)
- **RAM :** 4 GB (extensible à 8 GB)
- **Réseau :** 2x 1 Gbps (link aggregation)

#### Système
- **OS :** Synology DSM 7.x
- **Services :**
  - File Station
  - Hyper Backup
  - Snapshot Replication
  - Cloud Sync (Azure)

#### Volumes
- Volume1 : 12 TB (RAID 5)
  - /Backups-DC (4 TB)
  - /Backups-Web (4 TB)
  - /Backups-Docker (2 TB)
  - /Archives (2 TB)

#### Performance
- **Throughput lecture :** ~220 MB/s
- **Throughput écriture :** ~200 MB/s
- **IOPS :** 2000-3000 (RAID 5)

---

## 4. SERVICES ET APPLICATIONS

### 4.1 Active Directory

**Structure organisationnelle :**
```
ymmo.local
├── YMMO-Utilisateurs
│   ├── Direction (5 utilisateurs)
│   ├── Commercial (20 utilisateurs)
│   ├── Communication-Marketing (5 utilisateurs)
│   ├── RH-Juridique (5 utilisateurs)
│   └── IT-Support (5 utilisateurs)
├── YMMO-Ordinateurs
│   ├── PC-Siege (30 postes)
│   └── PC-Agences (60 postes, 5 par agence)
├── YMMO-Groupes
│   ├── GRP-Direction
│   ├── GRP-Commercial
│   ├── GRP-Communication-Marketing
│   ├── GRP-RH-Juridique
│   └── GRP-IT-Support
└── Domain Controllers
    └── DC-SIEGE
```

**GPO appliquées :**
- GPO-Securite-YMMO (politique mots de passe et verrouillage)
- Default Domain Policy (paramètres par défaut)

### 4.2 Application Web

**Fonctionnalités :**
- Gestion des biens immobiliers (CRUD)
- Gestion des clients et prospects
- Gestion des transactions
- Gestion des agents et agences
- Tableau de bord et statistiques
- Export de données (CSV, PDF)

**Technologies :**
- Frontend : HTML5, CSS3, JavaScript (vanilla ou framework léger)
- Backend : Python 3.x / Flask
- Base de données : MySQL 8.0
- Framework : Flask

**Base de données ymmo_db :**

Tables principales :
- utilisateurs (authentification)
- biens_immobiliers
- transactions
- clients
- agents_immobiliers
- agences
- rendez_vous
- documents (metadata)
- logs_activite

**Sécurité applicative :**
- Authentification par login/password (hashage bcrypt)
- Sessions sécurisées (secure cookies, HTTPS)
- Protection CSRF
- Validation et sanitisation des entrées
- Prepared statements (protection SQL injection)
- Principe du moindre privilège (rôles utilisateur)

### 4.3 Monitoring

#### Uptime Kuma
**Fonction :** Surveillance de disponibilité

**Monitors configurés :**
- Firewall Siège (ping, intervalle 60s)
- DC-SIEGE (ping, intervalle 60s)
- DNS Service (port 53, intervalle 60s)
- Serveur Web (HTTP check, intervalle 120s)
- MySQL (port 3306, intervalle 120s)
- 12 Agences (ping, intervalle 120s)

**Alertes :**
- Email vers it-support@ymmo.local
- Seuil : 2 échecs consécutifs

#### Zabbix
**Fonction :** Monitoring avancé système et réseau

**Hôtes monitorés :**
- DC-SIEGE (Zabbix Agent Windows)
- SRV-WEB-BDD (Zabbix Agent Linux)
- SRV-DOCKER-MONITORING (Zabbix Agent Linux)
- FW-SIEGE (SNMP)
- NAS-BACKUP (SNMP)

**Templates appliqués :**
- Template OS Windows by Zabbix agent
- Template OS Linux by Zabbix agent
- Template Net Network Generic Device SNMP

**Triggers critiques :**
- CPU usage > 80% for 5 min
- Memory usage > 85%
- Disk space < 20%
- Service down
- Host unreachable for 3 min

---

## 5. SÉCURITÉ

### 5.1 Sécurité réseau

#### Firewall OPNSense

**Configuration siège (10.0.0.1) :**

**Interfaces :**
- WAN (em0) : DHCP ou IP publique
- LAN (em1) : 10.0.0.1/24

**Politique par défaut :** Deny All

**Règles LAN → Internet :**
- Allow All (avec NAT/PAT)

**Règles LAN → LAN :**
1. Allow DHCP/DNS : UDP 53, 67-68 → 10.0.0.10
2. Allow AD Services : TCP/UDP 88, 135, 139, 389, 445, 464, 636, 3268, 3269 → 10.0.0.10
3. Allow Web : TCP 80, 443 → 10.0.0.11
4. Allow MySQL : TCP 3306 (source : 10.0.0.11 uniquement) → 10.0.0.11
5. Allow SMB : TCP 445 → 10.0.0.10, 10.0.0.11
6. Allow Monitoring : TCP 3001, 5001, 8080, 8081 → 10.0.0.12
7. Allow RDP : TCP 3389 → LAN net
8. Block All Other (implicite)

**Règles IPSec → LAN :**
- Allow All (trafic inter-sites autorisé)

#### VPN IPSec Site-à-Site

**Configuration :**
- Protocole : IKEv2
- Authentification : Pre-Shared Key (PSK)
- Phase 1 :
  - Chiffrement : AES-256
  - Hash : SHA-256
  - DH Group : 14 (2048 bits)
  - Lifetime : 28800s (8h)
- Phase 2 :
  - Chiffrement : AES-256-GCM
  - Hash : SHA-256
  - PFS : DH Group 14
  - Lifetime : 3600s (1h)

**Tunnels :**
- 12 tunnels (un par agence)
- Local subnet : 10.0.0.0/24
- Remote subnets : 10.1.0.0/24 à 10.12.0.0/24

**PSK (Pre-Shared Keys) :**
- Longueur : 32 caractères minimum
- Complexité : Majuscules + minuscules + chiffres + symboles
- Stockage : Coffre-fort de mots de passe
- Renouvellement : Annuel

### 5.2 Sécurité système

**Windows Server (DC-SIEGE) :**
- Windows Defender activé et à jour
- Firewall Windows activé
- Windows Update automatique (critiques uniquement)
- BitLocker (recommandé en production)
- Audit de sécurité activé
- Session RDP avec NLA obligatoire

**Linux Servers :**
- UFW (firewall) activé
- Fail2ban (protection bruteforce SSH)
- Unattended-upgrades (mises à jour auto sécurité)
- SSH : clés uniquement, root login désactivé, port 22
- SELinux/AppArmor activé
- LUKS disk encryption (recommandé en production)

### 5.3 GPO de sécurité

**GPO-Securite-YMMO :**

**Politique de mots de passe :**
- Longueur minimum : 8 caractères
- Complexité : Activée
- Durée max : 90 jours
- Durée min : 1 jour
- Historique : 5 mots de passe

**Verrouillage de compte :**
- Seuil : 5 tentatives
- Durée : 30 minutes
- Reset compteur : 30 minutes

**Audit :**
- Connexions : Succès et échecs
- Gestion comptes : Succès
- Accès objets : Échecs
- Modification stratégie : Succès

---

## 6. SAUVEGARDE ET DISPONIBILITÉ

### 6.1 Plan de sauvegarde

**Règle 3-2-1 :**
- 3 copies (production + NAS + cloud)
- 2 supports (disques + NAS)
- 1 hors site (Azure)

**Fréquence et rétention :**

| Système | Fréquence | Rétention | Destination |
|---------|-----------|-----------|-------------|
| AD System State | Quotidienne 02h00 | 14 jours | NAS + Azure |
| MySQL ymmo_db | Quotidienne 01h00 | 30 jours | NAS + Azure |
| Partages réseau | Quotidienne 03h00 | 90 jours | NAS + Azure |
| Config systèmes | Hebdomadaire Dim | 12 semaines | NAS |
| Snapshots VMs | Hebdomadaire Sam | 4 semaines | Local |

**Tests de restauration :**
- Fréquence : Mensuelle
- Objectif : Vérifier intégrité des sauvegardes
- Procédure : Restauration en environnement isolé

### 6.2 Objectifs de disponibilité

**RTO (Recovery Time Objective) :** 4 heures
- Temps maximum acceptable pour restaurer un service

**RPO (Recovery Point Objective) :** 24 heures
- Perte de données acceptable en cas de sinistre

**Disponibilité cible :** 99.5%
- Downtime maximum : 3.6 heures/mois

### 6.3 Haute disponibilité (Phase 2 - optionnel)

**Améliorations futures :**
- Contrôleur de domaine secondaire (redondance AD)
- Load balancing serveur web (HAProxy ou Traefik)
- Réplication MySQL maître-esclave
- Clustering OPNSense (CARP)

---

## 7. PERFORMANCES ET DIMENSIONNEMENT

### 7.1 Bande passante

**Siège :**
- Connexion Internet : 100 Mbps symétrique (fibre)
- Réseau interne : Gigabit (1000 Mbps)
- Trafic moyen : 20-30 Mbps
- Pics : 60-80 Mbps

**Agences :**
- Connexion Internet : 50 Mbps minimum
- Réseau interne : Gigabit
- Trafic moyen : 5-10 Mbps
- Pics : 20-30 Mbps

### 7.2 Latence

**Inter-sites (via VPN) :**
- Objectif : < 200ms
- Acceptable : < 300ms
- Critique si > 500ms

**Intra-site :**
- LAN : < 5ms
- Serveurs : < 2ms

### 7.3 Charge utilisateurs

**Concurrent users :**
- Application web : 50 utilisateurs simultanés
- Active Directory : 90 utilisateurs (tous)
- Partages fichiers : 30 utilisateurs simultanés

**Pics de charge :**
- Lundi matin : 8h-10h
- Vendredi après-midi : 14h-17h

---

## 8. MATÉRIEL ET BUDGET

### 8.1 Liste matériel production

#### Siège Aix-en-Provence

| Équipement | Quantité | Prix unitaire | Total |
|------------|----------|---------------|-------|
| Dell PowerEdge R240 (Serveur AD) | 1 | 3 500 € | 3 500 € |
| Dell PowerEdge R240 (Serveur Web) | 1 | 4 000 € | 4 000 € |
| HP ProLiant DL20 (Serveur Docker) | 1 | 3 000 € | 3 000 € |
| Synology DS920+ + 4x4TB | 1 | 2 000 € | 2 000 € |
| FortiGate 60F ou OPNSense Appliance | 1 | 2 500 € | 2 500 € |
| Cisco Catalyst 2960 24p | 1 | 1 500 € | 1 500 € |
| Onduleur APC 1500VA | 2 | 400 € | 800 € |
| Patch Panel + Câblage Cat6 | 1 | 500 € | 500 € |
| PC Dell OptiPlex (postes) | 30 | 700 € | 21 000 € |
| Imprimante HP LaserJet Pro | 1 | 400 € | 400 € |

**Subtotal Siège :** 39 200 €

#### Par Agence (x12)

| Équipement | Quantité | Prix unitaire | Total/agence | Total x12 |
|------------|----------|---------------|--------------|-----------|
| Firewall OPNSense APU2 | 1 | 300 € | 300 € | 3 600 € |
| Switch Netgear GS308 | 1 | 50 € | 50 € | 600 € |
| PC Dell OptiPlex | 5 | 700 € | 3 500 € | 42 000 € |
| Imprimante HP | 1 | 300 € | 300 € | 3 600 € |

**Subtotal par agence :** 4 150 €  
**Total 12 agences :** 49 800 €

### 8.2 Licences logicielles

| Licence | Quantité | Prix | Total |
|---------|----------|------|-------|
| Windows Server 2022 Standard | 1 | 1 000 € | 1 000 € |
| CAL Windows Server (utilisateurs) | 90 | 40 € | 3 600 € |
| Microsoft 365 Business (annuel) | 90 | 144 €/an | 12 960 €/an |

**Total licences initial :** 4 600 €  
**Total licences récurrent :** 12 960 €/an

### 8.3 Cloud et services

| Service | Coût mensuel | Coût annuel |
|---------|--------------|-------------|
| Azure Backup (500GB + DR) | 150 € | 1 800 € |
| Fibre 1Gbps siège | 200 € | 2 400 € |

**Total récurrent services :** 4 200 €/an

### 8.4 Budget total

**INVESTISSEMENT INITIAL :**
- Matériel siège : 39 200 €
- Matériel 12 agences : 49 800 €
- Licences logicielles : 4 600 €
- **TOTAL INITIAL : 93 600 €**

**COÛT RÉCURRENT ANNUEL :**
- Licences Microsoft 365 : 12 960 €
- Cloud et connectivité : 4 200 €
- **TOTAL ANNUEL : 17 160 €**

---

## 9. LIVRABLES

### 9.1 Documentation
- ✅ Cahier des charges technique
- ✅ Plan d'adressage IP
- ✅ Liste des services à déployer
- ✅ Matrice des droits d'accès
- ✅ Politique de sécurité
- ✅ Spécifications techniques (ce document)
- ✅ Schémas d'architecture réseau
- ✅ Guide de configuration des serveurs
- ✅ Plan de sauvegarde
- ✅ Procédures d'exploitation

### 9.2 Infrastructure
- ✅ 3 serveurs configurés et opérationnels
- ✅ Active Directory avec 90 utilisateurs
- ✅ 12 tunnels VPN IPSec fonctionnels
- ✅ Application web accessible
- ✅ Monitoring actif sur tous services
- ✅ Sauvegardes configurées et testées

---

## 10. CALENDRIER DE DÉPLOIEMENT

| Phase | Durée | Tâches |
|-------|-------|--------|
| **Phase 1** | Semaine 1 | Installation matériel siège, configuration réseau |
| **Phase 2** | Semaine 2 | Déploiement AD, DNS, DHCP, serveurs |
| **Phase 3** | Semaine 3 | Configuration VPN, interconnexion agences |
| **Phase 4** | Semaine 4 | Déploiement application web, tests |
| **Phase 5** | Semaine 5 | Monitoring, sauvegardes, sécurisation |
| **Phase 6** | Semaine 6 | Formation, documentation, mise en production |

---

## VALIDATION

**Document approuvé par :**
- Chef de projet INFRA : _______________
- Client YMMO : _______________
- Direction IT : _______________

**Date de validation :** _______________

---

**Version :** 1.0  
**Date :** Février 2026  
**Auteur :** Équipe IT Support YMMO  
**Statut :** Finalisé

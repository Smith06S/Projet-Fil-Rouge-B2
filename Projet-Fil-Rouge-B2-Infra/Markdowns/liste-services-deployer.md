# LISTE DES SERVICES À DÉPLOYER - INFRASTRUCTURE YMMO

**Projet :** Infrastructure YMMO  
**Version :** 1.0  
**Date :** Février 2026

---

## SERVEUR 1 - DC-SIEGE (10.0.0.10)

### Système d'exploitation
- **OS :** Windows Server 2022 Standard (Desktop Experience)
- **Version :** 21H2 ou supérieure
- **Licence :** 2 licences processeur + CAL utilisateurs

### Services Active Directory Domain Services

#### 1. Active Directory (AD DS)
**Description :** Service d'annuaire centralisé pour la gestion des utilisateurs et ressources

**Configuration :**
- Domaine : ymmo.local | NetBIOS : YMMO | Niveau : Windows Server 2022
- 90 utilisateurs répartis en 5 départements (Direction, Commercial, Marketing, RH, IT)
- OUs : YMMO-Utilisateurs, YMMO-Ordinateurs, YMMO-Groupes
- Groupes : GRP-Direction, GRP-Commercial, GRP-Communication-Marketing, GRP-RH-Juridique, GRP-IT-Support

*Pour les détails de configuration :* Voir [guide-configuration-serveurs.md](guide-configuration-serveurs.md#11-installation-dactive-directory)

**État :** ✅ Priorité 1 - Critique

---

#### 2. DNS Server
**Description :** Service de résolution de noms pour le domaine ymmo.local

**Configuration :** 
- Zone principale : ymmo.local (Active Directory-integrated)
- Zone inversée : 0.0.10.in-addr.arpa
- Redirecteurs : 8.8.8.8, 1.1.1.1
- Enregistrements : A (serveurs), SRV (services AD), CNAME (alias)

*Pour la liste complète des enregistrements DNS :* Voir [plan-adressage-ip.md](plan-adressage-ip.md#dns---enregistrements-principaux)

**État :** ✅ Priorité 1 - Critique

---

#### 3. DHCP Server
**Description :** Attribution automatique des adresses IP

**Configuration :** 
- Serveur : DC-SIEGE (10.0.0.10)
- Étendue Siège : 10.0.0.100 - 10.0.0.130 (31 adresses)
- Options : Gateway 10.0.0.1, DNS 10.0.0.10, Domaine ymmo.local
- Durée de bail : 8 jours
- Autorisation dans AD : Oui

*Pour les détails de configuration :* Voir [guide-configuration-serveurs.md](guide-configuration-serveurs.md#14-configuration-dhcp)

**État :** ✅ Priorité 1 - Critique

---

### Group Policy Objects (GPO)

#### 4. GPO-Securite-YMMO
**Description :** Politique de sécurité globale du domaine

**Configuration :** 
- Portée : ymmo.local (tous les utilisateurs et ordinateurs)
- Politique de mots de passe : Longueur 8 caractères, complexité, durée 90 jours
- Verrouillage : 5 tentatives, durée 30 minutes
- Audit : Connexions, gestion de comptes, accès objets

*Pour la configuration complète :* Voir [politique-securite.md](politique-securite.md#21-gestion-des-mots-de-passe)

**État :** ✅ Priorité 1 - Critique

---

### Partages réseau Windows

#### 5. Partages réseau Windows
**Description :** Dossiers partagés pour chaque département (Direction, Commercial, Marketing, RH, IT)

**Configuration :**
- Permissions NTFS : Selon rôles AD
- Accès réseau : \\DC-SIEGE\[NomPartage]
- Snapshots : Hourly snapshots, rétention 7 jours

*Pour la matrice complète des permissions :* Voir [matrice-droits-acces.md](matrice-droits-acces.md#21-partages-départementaux-serveur-dc-siege)

**État :** ✅ Priorité 2 - Important

---

#### 6. Windows Server Backup
**Description :** Sauvegarde du System State et données critiques

**Configuration :**
- Destination : NAS-BACKUP (\\10.0.0.20\Backups\DC-SIEGE)
- Fréquence : Quotidienne à 02h00
- Rétention : 7 jours
- Éléments : System State (AD, Registre), Partages, Configuration

*Pour le plan complet :* Voir [plan-sauvegarde-supervision.md](plan-sauvegarde-supervision.md)

**État :** ✅ Priorité 1 - Critique

---

## SERVEUR 2 - SRV-WEB-BDD (10.0.0.11)

### Système d'exploitation
- **OS :** Ubuntu Server 22.04 LTS
- **Kernel :** 5.15 ou supérieur
- **Architecture :** x86_64

### Services Web

#### 7. Apache HTTP Server 2.4
**Description :** Serveur HTTP et reverse proxy pour l'application YMMO

**Configuration :**
- Port : 80 (HTTP), 443 (HTTPS)
- Document Root : /var/www/html/ymmo
- Virtual Hosts : ymmo.local, www.ymmo.local
- Modules activés :
  - mod_rewrite
  - mod_ssl
  - mod_proxy
  - mod_proxy_http
  - mod_headers

**SSL/TLS :**
- Certificat : Auto-signé (LAB) ou Let's Encrypt (Production)
- Protocoles : TLSv1.2, TLSv1.3
- Ciphers : Forte sécurité (AES256-GCM-SHA384)

**État :** ✅ Priorité 1 - Critique

---

#### 8. Python 3.x / Flask
**Description :** Backend Python pour l'application web

**Accès :**
- Application servie par Flask
- Reverse proxy Apache vers Flask ou service WSGI

**Dependencies :**
- python3
- python3-pip
- python3-venv
- flask
- flask-cors
- python-dotenv
- mysqlclient

**Configuration :**
- Application installée dans un environnement virtuel
- Entrypoint : /var/www/html/ymmo/app.py
- Lancement via systemd ou Gunicorn

**État :** ✅ Priorité 1 - Critique

---

### Base de données

#### 9. MySQL 8.0 / MariaDB
**Description :** Système de gestion de base de données

**Configuration :**
- Port : 3306
- Bind address : 0.0.0.0 (accessible depuis le réseau)
- Charset : utf8mb4
- Collation : utf8mb4_unicode_ci

**Base de données principale :**
- Nom : ymmo_db
- Utilisateur : ymmo_user
- Mot de passe : [À définir - complexe]
- Privilèges : ALL sur ymmo_db.*

**Tables principales :**
- utilisateurs
- biens_immobiliers
- transactions
- clients
- agents_immobiliers
- agences
- rendez_vous
- documents
- logs_activite

**Sauvegardes :**
- Outil : mysqldump
- Fréquence : Quotidienne à 01h00
- Destination : /backup/mysql/ puis copie vers NAS
- Rétention : 14 jours

**État :** ✅ Priorité 1 - Critique

---

### Partages de fichiers

#### 10. Samba 4.x
**Description :** Partage de fichiers compatible Windows

**Configuration :**
- Workgroup : YMMO
- Security : user
- Intégration AD : Non (LAB) / Oui (Production)

**Partages Samba :**

| Partage | Chemin | Permissions |
|---------|--------|-------------|
| Documents-YMMO | /srv/samba/documents-ymmo | Authentification requise |
| Uploads-Web | /var/www/html/ymmo/uploads | Lecture: tous / Écriture: www-data |

**Utilisateurs Samba :**
- ymmo (mot de passe : ymmo123 - LAB uniquement)
- Synchronisation avec AD en production

**État :** ✅ Priorité 2 - Important

---

## SERVEUR 3 - SRV-DOCKER-MONITORING (10.0.0.12)

### Système d'exploitation
- **OS :** Ubuntu Server 22.04 LTS
- **Docker :** Docker Engine 24.x
- **Docker Compose :** v2.20 ou supérieur

### Services Docker

#### 11. Dockge
**Description :** Interface web pour gérer les stacks Docker Compose

**Configuration :** Image louislam/dockge:1, Port 5001, Volumes docker.sock + data
**Accès :** http://10.0.0.12:5001

**État :** ✅ Priorité 3 - Utile

---

#### 12. Traefik
**Description :** Reverse proxy et load balancer

**Configuration :** Image traefik:v2.11, Ports 80, 443, 8080, Providers Docker
**Fonctionnalités :** Routage automatique, HTTPS, Dashboard monitoring
**Accès dashboard :** http://10.0.0.12:8080

**État :** ✅ Priorité 3 - Utile

---

#### 13. Uptime Kuma
**Description :** Monitoring de disponibilité des services

**Monitors :** Firewall, DC-SIEGE, DNS Service, Serveur Web, MySQL, Agences (7 agences min)
**Notifications :** Email (it-support@ymmo.local), Webhooks Slack/Teams
**Accès :** http://10.0.0.12:3001

**État :** ✅ Priorité 2 - Important

---

#### 14. Zabbix
**Description :** Monitoring avancé de l'infrastructure

**Configuration :**
- Zabbix Server : zabbix/zabbix-server-pgsql:alpine-6.4
- Zabbix Web : zabbix/zabbix-web-nginx-pgsql:alpine-6.4
- PostgreSQL : postgres:15-alpine
- Port web : 8081

**Hôtes monitorés :**
- DC-SIEGE (10.0.0.10)
- SRV-WEB-BDD (10.0.0.11)
- SRV-DOCKER-MONITORING (10.0.0.12)
- FW-SIEGE (10.0.0.1)
- NAS-BACKUP (10.0.0.20)

**Templates appliqués :**
- Linux by Zabbix agent
- Windows by Zabbix agent
- ICMP Ping
- MySQL by Zabbix agent

**Métriques collectées :**
- CPU usage
- Memory usage
- Disk space
- Network traffic
- Process count
- Service status

**Alertes :**
- CPU > 80% pendant 5 min
- Memory > 85%
- Disk space < 20%
- Service down
- Host unreachable

**Accès :** http://10.0.0.12:8081  
**Login :** Admin / zabbix

**État :** ✅ Priorité 3 - Utile

---

## ÉQUIPEMENTS RÉSEAU

### Firewall Siège - FW-SIEGE (10.0.0.1)

#### 15. OPNSense
**Description :** Firewall open-source basé sur FreeBSD

**Configuration :**
- Interfaces : WAN (em0), LAN (em1) = 10.0.0.1/24
- Services activés : Firewall (pf), NAT/PAT, VPN IPSec, Tailscale
- Règles : LAN→WAN (Allow All), LAN→LAN (Services critiques uniquement), Block All Other

*Pour les règles détaillées :* Voir [specifications-techniques.md](specifications-techniques.md#51-sécurité-réseau) ou [guide-configuration-serveurs.md](guide-configuration-serveurs.md#44-configuration-dns-unbound)

**État :** ✅ Priorité 1 - Critique

---

#### 16. VPN IPSec Site-à-Site
**Description :** Interconnexion sécurisée du siège avec les 12 agences

**Configuration :**
- Protocole : IKEv2 | Chiffrement : AES-256-GCM | Hash : SHA-256
- DH Group : 14 | Lifetime Phase 1 : 28800s | Phase 2 : 3600s
- Tunnels : 12 (Paris, Lyon, Marseille, Bordeaux, Lille, Toulouse, Nantes, Strasbourg, Montpellier, Rennes, Nice, Grenoble)

*Pour les PSK et configuration détaillée :* Voir [specifications-techniques.md](specifications-techniques.md#vpn-ipsec-site-à-site)

**État :** ✅ Priorité 1 - Critique

---

#### 17. Tailscale VPN
**Description :** Accès distant sécurisé pour administration

**Utilisation :**
- Réservé IT Support + Direction (consultation)
- Administration firewall et serveurs à distance
- Accès aux services internes (Zabbix, Uptime Kuma, etc.)

*Pour la configuration complète :* Voir [politique-securite.md](politique-securite.md#32-accès-wifi-futur---phase-2)

**État :** ✅ Priorité 2 - Important

**Configuration :**
- Plugin : os-tailscale
- Advertise Routes : 10.0.0.0/24
- Accept Routes : Activé
- Exit Node : Non

**Utilisation :**
- Accès distant depuis l'école/domicile
- Administration firewall à distance
- Accès aux services internes

**État :** ✅ Priorité 2 - Important

---

### Firewalls Agences (x12)

#### 18. OPNSense Agences
**Description :** Firewall pour chaque agence (12 instances identiques)

**Configuration type :** 
- Interfaces : WAN (IP publique), LAN (10.x.0.1/24, x = 1-12)
- DHCP : Pool 10.x.0.100-110 (5 postes utilisés, 6 réservés)
- Règles : Similaires au siège, Allow VPN traffic depuis 10.0.0.0/24
- Tunnels VPN : Un tunnel IPSec vers le siège

**État :** ✅ Priorité 1 - Critique
- DHCP Server : Activé
  - Pool : 10.x.0.100 - 10.x.0.110
- VPN IPSec : Tunnel vers siège configuré

**État :** ✅ Priorité 1 - Critique

---

## NAS - NAS-BACKUP (10.0.0.20)

#### 19. Synology DSM
**Description :** Système de sauvegarde centralisée

**Services :**
- File Station : Gestion de fichiers
- Hyper Backup : Sauvegardes versionnées
- Snapshot Replication : Snapshots horaires
- Cloud Sync : Synchronisation Azure (optionnel)

**Partages NAS :**
- Backups-DC (DC-SIEGE)
- Backups-Web (SRV-WEB-BDD)
- Backups-Docker (SRV-DOCKER-MONITORING)
- Archives (documents anciens)

**Configuration RAID :**
- Type : RAID 5
- Disques : 4x 4TB
- Capacité utile : ~12TB

**État :** ✅ Priorité 1 - Critique

---

## RÉCAPITULATIF DES PRIORITÉS

### Priorité 1 - Critique (Déploiement immédiat)
- ✅ Active Directory (Service 1)
- ✅ DNS Server (Service 2)
- ✅ DHCP Server (Service 3)
- ✅ GPO-Securite-YMMO (Service 4)
- ✅ Apache HTTP (Service 7)
- ✅ Python/Flask (Service 8)
- ✅ MySQL (Service 9)
- ✅ OPNSense Siège (Service 15)
- ✅ VPN IPSec (Service 16)
- ✅ OPNSense Agences (Service 18)
- ✅ NAS Backup (Service 19)
- ✅ Windows Server Backup (Service 6)

### Priorité 2 - Important (Déploiement Semaine 2-3)
- ✅ Partages réseau (Service 5)
- ✅ Samba (Service 10)
- ✅ Uptime Kuma (Service 13)
- ✅ Tailscale (Service 17)

### Priorité 3 - Utile (Déploiement Semaine 4)
- ✅ Dockge (Service 11)
- ✅ Traefik (Service 12)
- ✅ Zabbix (Service 14)

---

## CALENDRIER DE DÉPLOIEMENT

| Semaine | Services à déployer |
|---------|---------------------|
| 1 | Services 1, 2, 3, 15 (AD, DNS, DHCP, Firewall) |
| 2 | Services 4, 7, 8, 9 (GPO, Web, Python/Flask, MySQL) |
| 3 | Services 5, 10, 16, 18 (Partages, Samba, VPN, Agences) |
| 4 | Services 6, 13, 19 (Backup, Monitoring, NAS) |
| 5 | Services 11, 12, 14, 17 (Docker, Traefik, Zabbix, Tailscale) |

---

**Responsable technique :** IT-Support YMMO  
**Version :** 1.0  
**Dernière mise à jour :** Février 2026

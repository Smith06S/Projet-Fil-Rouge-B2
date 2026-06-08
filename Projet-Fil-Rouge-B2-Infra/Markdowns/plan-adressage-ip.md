# PLAN D'ADRESSAGE IP - INFRASTRUCTURE YMMO

**Projet :** Infrastructure réseau YMMO  
**Version :** 1.0  
**Date :** Février 2026

---

## RÉCAPITULATIF GLOBAL

| Site | Réseau | Plage DHCP | Équipements fixes | Total IPs |
|------|--------|------------|-------------------|-----------|
| Siège Aix-en-Provence | 10.0.0.0/24 | 10.0.0.100-130 | 10.0.0.1-99 | 254 |
| Agence Paris | 10.1.0.0/24 | 10.1.0.100-110 | 10.1.0.1-10 | 254 |
| Agence Lyon | 10.2.0.0/24 | 10.2.0.100-110 | 10.2.0.1-10 | 254 |
| Agence Marseille | 10.3.0.0/24 | 10.3.0.100-110 | 10.3.0.1-10 | 254 |
| Agence Bordeaux | 10.4.0.0/24 | 10.4.0.100-110 | 10.4.0.1-10 | 254 |
| Agence Lille | 10.5.0.0/24 | 10.5.0.100-110 | 10.5.0.1-10 | 254 |
| Agence Toulouse | 10.6.0.0/24 | 10.6.0.100-110 | 10.6.0.1-10 | 254 |
| Agence Nantes | 10.7.0.0/24 | 10.7.0.100-110 | 10.7.0.1-10 | 254 |
| Agence Strasbourg | 10.8.0.0/24 | 10.8.0.100-110 | 10.8.0.1-10 | 254 |
| Agence Montpellier | 10.9.0.0/24 | 10.9.0.100-110 | 10.9.0.1-10 | 254 |
| Agence Rennes | 10.10.0.0/24 | 10.10.0.100-110 | 10.10.0.1-10 | 254 |
| Agence Nice | 10.11.0.0/24 | 10.11.0.100-110 | 10.11.0.1-10 | 254 |
| Agence Grenoble | 10.12.0.0/24 | 10.12.0.100-110 | 10.12.0.1-10 | 254 |
| Réseau VPN Management | 172.16.0.0/24 | - | 172.16.0.1-254 | 254 |

---

## SIÈGE AIX-EN-PROVENCE - 10.0.0.0/24

### Informations réseau
- **Réseau :** 10.0.0.0
- **Masque :** 255.255.255.0 (/24)
- **Passerelle :** 10.0.0.1
- **Broadcast :** 10.0.0.255
- **Adresses disponibles :** 254 (10.0.0.1 - 10.0.0.254)

### Infrastructure réseau (10.0.0.1 - 10.0.0.10)

| IP | Équipement | Hostname | Description |
|----|------------|----------|-------------|
| 10.0.0.1 | Firewall | FW-SIEGE | OPNSense - Interface LAN |
| 10.0.0.2 | Switch Core | SW-CORE-01 | Cisco Catalyst 2960 24 ports |
| 10.0.0.3 | - | - | Réservé (Switch Core backup) |
| 10.0.0.4 | - | - | Réservé |
| 10.0.0.5 | - | - | Réservé |
| 10.0.0.6 | - | - | Réservé |
| 10.0.0.7 | - | - | Réservé |
| 10.0.0.8 | - | - | Réservé |
| 10.0.0.9 | - | - | Réservé |
| 10.0.0.10 | Serveur | DC-SIEGE | Windows Server 2022 - AD/DNS/DHCP |

### Serveurs (10.0.0.11 - 10.0.0.30)

| IP | Équipement | Hostname | Description |
|----|------------|----------|-------------|
| 10.0.0.11 | Serveur | SRV-WEB-BDD | Ubuntu Server - Apache/MySQL/Samba |
| 10.0.0.12 | Serveur | SRV-DOCKER-MONITORING | Ubuntu Server - Docker/Monitoring |
| 10.0.0.13 | - | - | Réservé (Serveur futur) |
| 10.0.0.14 | - | - | Réservé (Serveur futur) |
| 10.0.0.15 | - | - | Réservé (Serveur futur) |
| 10.0.0.20 | NAS | NAS-BACKUP | Synology DS920+ - Sauvegarde |
| 10.0.0.21 | - | - | Réservé (NAS futur) |
| 10.0.0.22-30 | - | - | Réservé |

### Équipements spéciaux (10.0.0.31 - 10.0.0.50)

| IP | Équipement | Hostname | Description |
|----|------------|----------|-------------|
| 10.0.0.31 | - | - | Réservé (Téléphonie VoIP) |
| 10.0.0.32 | - | - | Réservé (Téléphonie VoIP) |
| 10.0.0.40 | - | - | Réservé (Caméras IP) |
| 10.0.0.41 | - | - | Réservé (Caméras IP) |
| 10.0.0.50 | - | - | Réservé (Point d'accès WiFi) |

### Réservé expansion (10.0.0.51 - 10.0.0.99)

| Plage | Usage |
|-------|-------|
| 10.0.0.51 - 10.0.0.99 | Réservé pour extensions futures |

### Pool DHCP - Postes de travail (10.0.0.100 - 10.0.0.130)

| Plage | Usage | Nombre |
|-------|-------|--------|
| 10.0.0.100 - 10.0.0.130 | Postes de travail siège | 31 adresses |

**Configuration DHCP :**
- Serveur DHCP : 10.0.0.10 (DC-SIEGE)
- Passerelle par défaut : 10.0.0.1
- Serveur DNS : 10.0.0.10
- Domaine DNS : ymmo.local
- Durée de bail : 8 jours

**Répartition estimée :**
- Direction : 5 postes (10.0.0.100-104)
- Commercial : 10 postes (10.0.0.105-114)
- Communication-Marketing : 5 postes (10.0.0.115-119)
- RH-Juridique : 5 postes (10.0.0.120-124)
- IT-Support : 5 postes (10.0.0.125-129)
- Invités : 1 adresse (10.0.0.130)

### Réservé (10.0.0.131 - 10.0.0.199)

| Plage | Usage |
|-------|-------|
| 10.0.0.131 - 10.0.0.199 | Réservé pour expansion DHCP future |

### Imprimantes et périphériques (10.0.0.200 - 10.0.0.210)

| IP | Équipement | Hostname | Description |
|----|------------|----------|-------------|
| 10.0.0.200 | Imprimante | PRINT-SIEGE-01 | HP LaserJet Pro M404dn |
| 10.0.0.201 | Imprimante | PRINT-SIEGE-02 | Réservé (Imprimante couleur) |
| 10.0.0.202-210 | - | - | Réservé (Scanners, autres périphériques) |

### Réservé (10.0.0.211 - 10.0.0.254)

| Plage | Usage |
|-------|-------|
| 10.0.0.211 - 10.0.0.254 | Réservé |

---

## AGENCE PARIS - 10.1.0.0/24

### Informations réseau
- **Réseau :** 10.1.0.0
- **Masque :** 255.255.255.0 (/24)
- **Passerelle :** 10.1.0.1
- **Broadcast :** 10.1.0.255

### Infrastructure (10.1.0.1 - 10.1.0.10)

| IP | Équipement | Description |
|----|------------|-------------|
| 10.1.0.1 | Firewall OPNSense | Interface LAN + DHCP Server |
| 10.1.0.2 | Switch 8 ports | Netgear GS308 |
| 10.1.0.3-10 | - | Réservé |

### Pool DHCP (10.1.0.100 - 10.1.0.110)

| Plage | Usage | Nombre |
|-------|-------|--------|
| 10.1.0.100 - 10.1.0.110 | Postes commerciaux | 11 adresses (5 utilisés, 6 réservés) |

**Configuration DHCP locale :**
- Serveur DHCP : 10.1.0.1 (OPNSense)
- Passerelle : 10.1.0.1
- DNS : 10.0.0.10 (via VPN)
- Domaine : ymmo.local

### Périphériques (10.1.0.200 - 10.1.0.210)

| IP | Équipement | Description |
|----|------------|-------------|
| 10.1.0.200 | Imprimante | HP LaserJet |
| 10.1.0.201-210 | - | Réservé |

---

## AGENCE LYON - 10.2.0.0/24

### Configuration identique à Agence Paris

| IP | Équipement | Description |
|----|------------|-------------|
| 10.2.0.1 | Firewall OPNSense | Interface LAN + DHCP |
| 10.2.0.2 | Switch 8 ports | Netgear GS308 |
| 10.2.0.100-110 | DHCP Pool | Postes commerciaux |
| 10.2.0.200 | Imprimante | HP LaserJet |

---

## AGENCE MARSEILLE - 10.3.0.0/24

| IP | Équipement | Description |
|----|------------|-------------|
| 10.3.0.1 | Firewall OPNSense | Interface LAN + DHCP |
| 10.3.0.2 | Switch 8 ports | Netgear GS308 |
| 10.3.0.100-110 | DHCP Pool | Postes commerciaux |
| 10.3.0.200 | Imprimante | HP LaserJet |

---

## AGENCE BORDEAUX - 10.4.0.0/24

| IP | Équipement | Description |
|----|------------|-------------|
| 10.4.0.1 | Firewall OPNSense | Interface LAN + DHCP |
| 10.4.0.2 | Switch 8 ports | Netgear GS308 |
| 10.4.0.100-110 | DHCP Pool | Postes commerciaux |
| 10.4.0.200 | Imprimante | HP LaserJet |

---

## AGENCE LILLE - 10.5.0.0/24

| IP | Équipement | Description |
|----|------------|-------------|
| 10.5.0.1 | Firewall OPNSense | Interface LAN + DHCP |
| 10.5.0.2 | Switch 8 ports | Netgear GS308 |
| 10.5.0.100-110 | DHCP Pool | Postes commerciaux |
| 10.5.0.200 | Imprimante | HP LaserJet |

---

## AGENCE TOULOUSE - 10.6.0.0/24

| IP | Équipement | Description |
|----|------------|-------------|
| 10.6.0.1 | Firewall OPNSense | Interface LAN + DHCP |
| 10.6.0.2 | Switch 8 ports | Netgear GS308 |
| 10.6.0.100-110 | DHCP Pool | Postes commerciaux |
| 10.6.0.200 | Imprimante | HP LaserJet |

---

## AGENCE NANTES - 10.7.0.0/24

| IP | Équipement | Description |
|----|------------|-------------|
| 10.7.0.1 | Firewall OPNSense | Interface LAN + DHCP |
| 10.7.0.2 | Switch 8 ports | Netgear GS308 |
| 10.7.0.100-110 | DHCP Pool | Postes commerciaux |
| 10.7.0.200 | Imprimante | HP LaserJet |

---

## AGENCE STRASBOURG - 10.8.0.0/24

| IP | Équipement | Description |
|----|------------|-------------|
| 10.8.0.1 | Firewall OPNSense | Interface LAN + DHCP |
| 10.8.0.2 | Switch 8 ports | Netgear GS308 |
| 10.8.0.100-110 | DHCP Pool | Postes commerciaux |
| 10.8.0.200 | Imprimante | HP LaserJet |

---

## AGENCE MONTPELLIER - 10.9.0.0/24

| IP | Équipement | Description |
|----|------------|-------------|
| 10.9.0.1 | Firewall OPNSense | Interface LAN + DHCP |
| 10.9.0.2 | Switch 8 ports | Netgear GS308 |
| 10.9.0.100-110 | DHCP Pool | Postes commerciaux |
| 10.9.0.200 | Imprimante | HP LaserJet |

---

## AGENCE RENNES - 10.10.0.0/24

| IP | Équipement | Description |
|----|------------|-------------|
| 10.10.0.1 | Firewall OPNSense | Interface LAN + DHCP |
| 10.10.0.2 | Switch 8 ports | Netgear GS308 |
| 10.10.0.100-110 | DHCP Pool | Postes commerciaux |
| 10.10.0.200 | Imprimante | HP LaserJet |

---

## AGENCE NICE - 10.11.0.0/24

| IP | Équipement | Description |
|----|------------|-------------|
| 10.11.0.1 | Firewall OPNSense | Interface LAN + DHCP |
| 10.11.0.2 | Switch 8 ports | Netgear GS308 |
| 10.11.0.100-110 | DHCP Pool | Postes commerciaux |
| 10.11.0.200 | Imprimante | HP LaserJet |

---

## AGENCE GRENOBLE - 10.12.0.0/24

| IP | Équipement | Description |
|----|------------|-------------|
| 10.12.0.1 | Firewall OPNSense | Interface LAN + DHCP |
| 10.12.0.2 | Switch 8 ports | Netgear GS308 |
| 10.12.0.100-110 | DHCP Pool | Postes commerciaux |
| 10.12.0.200 | Imprimante | HP LaserJet |

---

## RÉSEAU VPN MANAGEMENT - 172.16.0.0/24

### Informations
- **Usage :** Gestion des tunnels VPN IPSec
- **Réseau :** 172.16.0.0/24
- **Masque :** 255.255.255.0

### Adresses virtuelles VPN

| IP | Site | Description |
|----|------|-------------|
| 172.16.0.1 | Siège | Endpoint VPN principal |
| 172.16.0.10 | Agence Paris | Endpoint VPN |
| 172.16.0.11 | Agence Lyon | Endpoint VPN |
| 172.16.0.12 | Agence Marseille | Endpoint VPN |
| 172.16.0.13 | Agence Bordeaux | Endpoint VPN |
| 172.16.0.14 | Agence Lille | Endpoint VPN |
| 172.16.0.15 | Agence Toulouse | Endpoint VPN |
| 172.16.0.16 | Agence Nantes | Endpoint VPN |
| 172.16.0.17 | Agence Strasbourg | Endpoint VPN |
| 172.16.0.18 | Agence Montpellier | Endpoint VPN |
| 172.16.0.19 | Agence Rennes | Endpoint VPN |
| 172.16.0.20 | Agence Nice | Endpoint VPN |
| 172.16.0.21 | Agence Grenoble | Endpoint VPN |

---

## RÉSUMÉ DES VLANS (OPTIONNEL - Phase 2)

### VLAN Siège (si implémenté)

| VLAN ID | Nom | Réseau | Usage |
|---------|-----|--------|-------|
| 10 | VLAN-SERVEURS | 10.0.0.0/24 | Serveurs et infrastructure |
| 20 | VLAN-UTILISATEURS | 10.0.1.0/24 | Postes de travail (futur) |
| 30 | VLAN-INVITES | 10.0.2.0/24 | Accès invités WiFi (futur) |
| 40 | VLAN-VOIP | 10.0.3.0/24 | Téléphonie IP (futur) |
| 99 | VLAN-MANAGEMENT | 192.168.99.0/24 | Gestion des équipements |

---

## CONVENTIONS DE NOMMAGE

### Serveurs
- Format : `[TYPE]-[FONCTION]-[NUMERO]`
- Exemples : DC-SIEGE, SRV-WEB-BDD, SRV-DOCKER-MONITORING

### Firewalls
- Format : `FW-[SITE]`
- Exemples : FW-SIEGE, FW-PARIS, FW-LYON

### Switches
- Format : `SW-[TYPE]-[NUMERO]`
- Exemples : SW-CORE-01, SW-ACCESS-01

### Postes de travail
- Format : `PC-[SITE]-[DEPT]-[NUMERO]`
- Exemples : PC-SIEGE-DIR-01, PC-PARIS-COM-01

### Imprimantes
- Format : `PRINT-[SITE]-[NUMERO]`
- Exemples : PRINT-SIEGE-01, PRINT-PARIS-01

---

## DNS - ENREGISTREMENTS PRINCIPAUX

### Zone ymmo.local

| Nom | Type | IP | Description |
|-----|------|----|--------------|
| @ | A | 10.0.0.10 | Domaine principal |
| dc-siege | A | 10.0.0.10 | Contrôleur de domaine |
| srv-web-bdd | A | 10.0.0.11 | Serveur web et BDD |
| srv-docker-monitoring | A | 10.0.0.12 | Serveur Docker |
| nas-backup | A | 10.0.0.20 | NAS sauvegarde |
| fw-siege | A | 10.0.0.1 | Firewall siège |
| www | CNAME | srv-web-bdd | Alias serveur web |
| monitoring | CNAME | srv-docker-monitoring | Alias monitoring |
| _ldap._tcp | SRV | dc-siege:389 | Service LDAP |
| _kerberos._tcp | SRV | dc-siege:88 | Service Kerberos |

---

## RÈGLES DE GESTION

### Attribution d'adresses IP

1. **Adresses fixes (1-99) :**
   - Toujours configurées manuellement
   - Documentées dans ce plan
   - Pas de DHCP sur cette plage

2. **Pool DHCP (100-199) :**
   - Attribution automatique
   - Réservations DHCP pour équipements critiques
   - Durée de bail : 8 jours

3. **Périphériques (200-210) :**
   - IP fixes configurées manuellement
   - Réservées pour imprimantes, scanners, etc.

4. **Réservé (211-254) :**
   - Pas d'attribution
   - Disponible pour expansion future

### Modifications du plan

Toute modification doit être :
1. Documentée dans ce fichier (version Git)
2. Mise à jour dans le DNS
3. Communiquée à l'équipe IT
4. Testée avant mise en production

---

## CONTACT

**Responsable réseau :** IT-Support YMMO  
**Email :** it-support@ymmo.local  
**Téléphone :** +33 X XX XX XX XX

---

**Version :** 1.0  
**Dernière mise à jour :** Février 2026  
**Prochaine révision :** Août 2026

# Guide de Déploiement - YMMO Immobilier

## 1. Prérequis de Déploiement

### 1.1 Matériel Requis

```
Hyperviseur :
- VMware Workstation Pro 17+ (PC personnel)
- RAM hôte minimum : 16 GB (recommandé 32 GB)
- Disque dur : 500 GB SSD (10 000 tr/min minimum)
- CPU : Intel i7/i9 ou AMD Ryzen 7/9

Réseau :
- Connexion internet stable (10 Mbps minimum)
- Accès VPN Tailscale (pour école/distanciel)
- Switch virtuel pour inter-VM
```

### 1.2 Logiciels Requis

```
Sur le poste de développement :
- VMware Workstation Pro 17.x
- Putty / MobaXterm (terminal SSH)
- Visual Studio Code (édition fichiers)
- Git + GitHub Desktop
- VNC Viewer (accès aux VMs)
```

### 1.3 Images OS Requises

```
- Windows Server 2022 ISO
- Ubuntu 22.04 LTS ISO
- OPNSense 24.x ISO
```

### 1.4 Comptes et Licences

```
- Compte GitHub (pour versionning)
- Compte Tailscale (VPN gratuit pour petits réseaux)
- License VMware Workstation Pro (60€)
```

---

## 2. Architecture de Déploiement

### 2.1 Schéma des Réseaux VMware

```
┌─────────────────────────────────────────┐
│      VMware Workstation Pro             │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  VMnet2 (Réseau Siège)           │  │
│  │  10.0.0.0/24                    │  │
│  │  ┌────────────────────────────┐ │  │
│  │  │ OPNSense (10.0.0.1)       │ │  │
│  │  │ DC-SIEGE (10.0.0.10)      │ │  │
│  │  │ SRV-WEB-BDD (10.0.0.11)   │ │  │
│  │  │ SRV-Docker (10.0.0.12)    │ │  │
│  │  │ NAS-Backup (10.0.0.20)    │ │  │
│  │  └────────────────────────────┘ │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  VMnet3 (Agence Paris)           │  │
│  │  10.1.0.0/24                    │  │
│  │  ┌────────────────────────────┐ │  │
│  │  │ OPNSense-Agence (10.1.0.1)│ │  │
│  │  │ Agence-PC (DHCP)           │ │  │
│  │  └────────────────────────────┘ │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  VMnet4 (Agence Lyon - Opt.)     │  │
│  │  10.2.0.0/24                    │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### 2.2 Spécifications des VMs

| VM | OS | CPU | RAM | Disque | Rôle |
|----|-----|-----|-----|--------|------|
| OPNSense-Siège | OPNSense 24 | 2 | 2 GB | 20 GB | Firewall/Router |
| DC-SIEGE | Windows Server 2022 | 2 | 4 GB | 40 GB | AD/DNS/DHCP |
| SRV-WEB-BDD | Ubuntu 22.04 | 2 | 4 GB | 50 GB | Web/MySQL |
| SRV-Docker | Ubuntu 22.04 | 4 | 8 GB | 100 GB | Docker/Monitoring |
| OPNSense-Agence | OPNSense 24 | 2 | 2 GB | 20 GB | Firewall agence |
| NAS-Backup | TrueNAS Core | 2 | 2 GB | 100 GB | Stockage backups |

---

## 3. Checklist de Déploiement

### 3.1 Phase 0 : Préparation Environnement

```
[ ] Vérifier l'espace disque disponible (> 500 GB)
[ ] Télécharger les ISO OS
[ ] Créer les dossiers de VMs
[ ] Configurer VMware réseau
[ ] Tester l'accès Tailscale
[ ] Créer les répertoires partagés
[ ] Préparer les scripts de déploiement
```

### 3.2 Phase 1 : Déploiement Infrastructure (Jour 1)

#### Étape 1 : OPNSense Siège

```
[ ] Créer VM OPNSense-Siège
    - 2 vCPU, 2 GB RAM, 20 GB disque
    - Adapter 1 : NAT (WAN - vers hôte)
    - Adapter 2 : VMnet2 (LAN - siège)

[ ] Installer OPNSense
    - Installer depuis ISO
    - Configuration de base
    - IP LAN : 10.0.0.1/24

[ ] Configurer Unbound DNS
    - Ajouter enregistrements DNS (ymmo.immo, etc.)
    - Vérifier résolution

[ ] Configurer Firewall
    - Règles basiques (Allow LAN)
    - Règle DHCP (optionnel)

[ ] Tester
    - ping 10.0.0.1
    - Accès Web https://10.0.0.1
```

#### Étape 2 : DC-SIEGE

```
[ ] Créer VM DC-SIEGE
    - 2 vCPU, 4 GB RAM, 40 GB disque
    - Adapter : VMnet2
    - IP statique : 10.0.0.10/24

[ ] Installer Windows Server 2022
    - Configuration basique
    - Hostname : DC-SIEGE
    - IP : 10.0.0.10, Gateway : 10.0.0.1

[ ] Installer Active Directory
    Install-ADDSForest -DomainName "ymmo.local"
    
[ ] Configurer DHCP et DNS
    - Ajouter scope DHCP
    - Enregistrements DNS

[ ] Tester
    - ping DC-SIEGE
    - nslookup ymmo.local
```

#### Étape 3 : SRV-WEB-BDD

```
[ ] Créer VM SRV-WEB-BDD
    - 2 vCPU, 4 GB RAM, 50 GB disque
    - Adapter : VMnet2
    - IP statique : 10.0.0.11/24

[ ] Installer Ubuntu 22.04
    - Configuration réseau statique
    - Hostname : srv-web-bdd
    - DNS : 10.0.0.1

[ ] Installer Services
    sudo apt install apache2 mysql-server python3-pip

[ ] Déployer Application
    - Copier application Flask
    - Configurer systemd service
    - Démarrer l'application

[ ] Tester
    - curl http://10.0.0.11
    - curl http://ymmo.immo
```

#### Étape 4 : SRV-Docker-Monitoring

```
[ ] Créer VM SRV-Docker
    - 4 vCPU, 8 GB RAM, 100 GB disque
    - Adapter : VMnet2
    - IP statique : 10.0.0.12/24

[ ] Installer Ubuntu 22.04
    - Configuration réseau
    - Hostname : srv-docker-monitoring

[ ] Installer Docker
    curl -fsSL https://get.docker.com | sudo sh

[ ] Déployer Dockge
    docker run -d \
      -p 5001:5001 \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v ~/docker/dockge:/app/data \
      louislam/dockge:latest

[ ] Créer Stacks Docker
    - Traefik
    - Uptime Kuma
    - Zabbix

[ ] Configurer Zabbix Agent
    sudo apt install zabbix-agent2

[ ] Tester
    - http://10.0.0.12:5001 (Dockge)
    - http://10.0.0.12:8080 (Traefik)
    - http://10.0.0.12:3001 (Uptime Kuma)
    - http://10.0.0.12:8081 (Zabbix)
```

### 3.3 Phase 2 : Déploiement Agences (Jour 2)

#### Étape 5 : OPNSense Agence Paris

```
[ ] Créer VM OPNSense-Agence
    - 2 vCPU, 2 GB RAM, 20 GB disque
    - Adapter 1 : NAT (WAN)
    - Adapter 2 : VMnet3 (LAN agence)

[ ] Configurer OPNSense
    - IP LAN : 10.1.0.1/24
    - DHCP pool : 10.1.0.100-110
    - DNS : Pointer vers DC-SIEGE (10.0.0.10)

[ ] Configurer VPN IPSec
    - Tunnels vers OPNSense siège
    - Phase 1 & 2 IKEv2/AES-256-GCM

[ ] Configurer Firewall
    - Allow VPN traffic
    - Block external non-established

[ ] Tester
    - ping siège depuis agence (10.0.0.1 via VPN)
    - Résolution DNS fonctionnelle
```

#### Étape 6 : Validation et Tests

```
[ ] Tests de Connectivité
    - [ ] Siège ↔ Agence Paris (VPN)
    - [ ] Résolution DNS (nslookup)
    - [ ] Accès aux services web

[ ] Tests de Disponibilité
    - [ ] Chaque service respond au ping
    - [ ] Chaque port TCP accessible
    - [ ] DNS résout tous les noms

[ ] Tests de Performance
    - [ ] Latence réseau < 50ms (local)
    - [ ] Latence VPN < 100ms
    - [ ] Bande passante > 1 Mbps

[ ] Vérification Supervisoins
    - [ ] Uptime Kuma : 5/5 monitors verts
    - [ ] Zabbix : Ubuntu-Docker connected
    - [ ] Aucune alerte CRITICAL
```

---

## 4. Scripts d'Automatisation

### 4.1 Script PowerShell : Déployer AD

**Fichier : deploy-ad.ps1**

```powershell
# Script de déploiement Active Directory

# Paramètres
$DomainName = "ymmo.local"
$NetbiosName = "YMMO"
$DSRMPassword = "DSRM123!"

# Convertir mot de passe
$SecurePassword = ConvertTo-SecureString $DSRMPassword -AsPlainText -Force

# Installer le rôle
Write-Host "Installation d'Active Directory..."
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools

# Promouvoir en DC
Write-Host "Promotion en contrôleur de domaine..."
Install-ADDSForest `
  -DomainName $DomainName `
  -DomainNetbiosName $NetbiosName `
  -InstallDns `
  -SafeModeAdministratorPassword $SecurePassword `
  -Force

Write-Host "Déploiement AD terminé!"
Write-Host "La VM va redémarrer..."
```

**Utilisation :**
```powershell
powershell -ExecutionPolicy Bypass -File deploy-ad.ps1
```

### 4.2 Script Bash : Déployer SRV-WEB-BDD

**Fichier : deploy-web-bdd.sh**

```bash
#!/bin/bash
# Script de déploiement SRV-WEB-BDD

set -e  # Exit on error

echo "=== Déploiement SRV-WEB-BDD ==="

# Mise à jour système
echo "[1/6] Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# Installation services
echo "[2/6] Installation Apache + MySQL + Python..."
sudo apt install apache2 mysql-server python3-pip -y

# Activation services
echo "[3/6] Activation des services..."
sudo systemctl enable apache2
sudo systemctl enable mysql
sudo systemctl start apache2
sudo systemctl start mysql

# Installation application
echo "[4/6] Déploiement application Flask..."
mkdir -p /var/www/html/ymmo
cd /var/www/html/Projet-Fil-Rouge-B2_copie
pip3 install -r requirements.txt 2>/dev/null || pip3 install flask

# Configuration systemd
echo "[5/6] Configuration du service systemd..."
sudo bash -c 'cat > /etc/systemd/system/ymmo-app.service << EOF
[Unit]
Description=YMMO Flask App
After=network.target

[Service]
Type=simple
User=ymmo
WorkingDirectory=/var/www/html/Projet-Fil-Rouge-B2_copie
ExecStart=/usr/bin/python3 /var/www/html/Projet-Fil-Rouge-B2_copie/app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl daemon-reload
sudo systemctl enable ymmo-app.service
sudo systemctl start ymmo-app.service

# Vérification
echo "[6/6] Vérification..."
sleep 2
curl http://localhost:5000 > /dev/null && echo "✓ Application Flask est UP"
sudo systemctl status apache2 | grep -q "active" && echo "✓ Apache est UP"
sudo systemctl status mysql | grep -q "active" && echo "✓ MySQL est UP"

echo ""
echo "=== Déploiement terminé ! ==="
echo "URL d'accès : http://10.0.0.11:5000"
```

**Utilisation :**
```bash
chmod +x deploy-web-bdd.sh
./deploy-web-bdd.sh
```

### 4.3 Script Bash : Déployer Docker

**Fichier : deploy-docker.sh**

```bash
#!/bin/bash
# Script de déploiement SRV-Docker

set -e

echo "=== Déploiement SRV-Docker-Monitoring ==="

# Installation Docker
echo "[1/4] Installation Docker..."
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
newgrp docker

# Création répertoires
echo "[2/4] Création des répertoires..."
mkdir -p ~/docker/dockge ~/docker/stacks/{traefik,uptime-kuma,zabbix}

# Lancement Dockge
echo "[3/4] Déploiement Dockge..."
docker run -d \
  --name dockge \
  -p 5001:5001 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/docker/dockge:/app/data \
  louislam/dockge:latest

# Installation Zabbix Agent
echo "[4/4] Installation Zabbix Agent..."
sudo apt install zabbix-agent2 -y

# Configuration Zabbix Agent
sudo bash -c 'cat > /etc/zabbix/zabbix_agent2.conf << EOF
Server=localhost
ServerActive=localhost:10051
Hostname=Ubuntu-Docker
ListenPort=10050
DebugLevel=3
EOF'

sudo systemctl enable zabbix-agent2
sudo systemctl restart zabbix-agent2

echo ""
echo "=== Déploiement Docker terminé ! ==="
echo "Dockge : http://10.0.0.12:5001"
echo "Veuillez créer les stacks (Traefik, Uptime Kuma, Zabbix) via Dockge"
```

---

## 5. Tests de Validation

### 5.1 Test de Connectivité Réseau

```bash
#!/bin/bash
# test-connectivity.sh

echo "=== Test de connectivité YMMO ==="

targets=(
  "10.0.0.1:OPNSense"
  "10.0.0.10:DC-SIEGE"
  "10.0.0.11:SRV-WEB-BDD"
  "10.0.0.12:SRV-Docker"
)

for target in "${targets[@]}"; do
  ip="${target%:*}"
  name="${target#*:}"
  
  if ping -c 1 -W 1 "$ip" > /dev/null 2>&1; then
    echo "✓ $name ($ip) - ONLINE"
  else
    echo "✗ $name ($ip) - OFFLINE"
  fi
done

# Test DNS
echo ""
echo "=== Test DNS ==="
for domain in "ymmo.immo" "dc-siege.ymmo.local" "srv-docker-monitoring.ymmo.local"; do
  if nslookup "$domain" 10.0.0.1 > /dev/null 2>&1; then
    echo "✓ $domain"
  else
    echo "✗ $domain - NOT RESOLVED"
  fi
done

# Test Services Web
echo ""
echo "=== Test Services Web ==="
urls=(
  "http://10.0.0.11:Accueil%20Web"
  "http://10.0.0.12:5001:Dockge"
  "http://10.0.0.12:8080:Traefik"
  "http://10.0.0.12:3001:Uptime%20Kuma"
  "http://10.0.0.12:8081:Zabbix"
)

for url in "${urls[@]}"; do
  path="${url%:*}"
  name="${url#*:}"
  
  if curl -s -o /dev/null -w "%{http_code}" "$path" | grep -q "200\|301\|302"; then
    echo "✓ $name - ACCESSIBLE"
  else
    echo "✗ $name - NOT ACCESSIBLE"
  fi
done
```

### 5.2 Checklist Finale

```
Infrastructure:
[ ] Tous les pings répondent
[ ] DNS résout tous les domaines
[ ] Tous les services web accessibles

Active Directory:
[ ] Domaine ymmo.local créé
[ ] Utilisateurs créés
[ ] Groupes créés
[ ] Réplication avec DC-SIEGE-02 (si présent)

Services Web:
[ ] Application Flask UP et accessible
[ ] Apache accepte les connexions
[ ] MySQL database créée

Docker/Monitoring:
[ ] Dockge accessible
[ ] Traefik dashboard visible
[ ] Uptime Kuma: 5/5 monitors verts
[ ] Zabbix: Ubuntu-Docker connected

Réseau VPN:
[ ] VPN IPSec site-to-site établi
[ ] Communication siège ↔ agence testée
[ ] Latence VPN < 100ms

Backups:
[ ] Script de sauvegarde fonctionne
[ ] Dernière sauvegarde < 24h
[ ] Espace disque NAS > 50 %
```

---

## 6. Procédures de Maintenance Post-Déploiement

### 6.1 Maintenance Quotidienne

```bash
# Vérifier l'état des services
sudo systemctl status apache2 mysql docker zabbix-agent2

# Vérifier les logs de la journée
sudo journalctl -u ymmo-app.service -n 50
sudo tail -50 /var/log/syslog

# Vérifier les sauvegardes
ls -lh /mnt/backup/
```

### 6.2 Maintenance Hebdomadaire

```bash
# Vérifier l'espace disque
df -h /

# Vérifier la santé des VMs
vmrun list  # VMware command

# Vérifier les alertes Zabbix
# Via interface Web : http://10.0.0.12:8081
```

### 6.3 Maintenance Mensuelle

```powershell
# Sur DC-SIEGE - Vérifier réplication AD
repadmin /showrepl
dcdiag /v

# Tester une restauration de sauvegarde
# Effectuer un test complet de RTO/RPO
```

---

## 7. Troubleshooting Courant

### 7.1 OPNSense

| Problème | Cause | Solution |
|---------|-------|----------|
| Pas d'accès HTTPS | Certificat invalide | Télécharger le certificat OPNSense |
| DNS ne résout pas | Unbound désactivé | Relancer Unbound via Services |
| VPN ne se connecte | PSK incorrect | Vérifier PSK dans OPNSense et config IKEv2 |

### 7.2 Active Directory

| Problème | Cause | Solution |
|---------|-------|----------|
| Domaine non trouvé | AD pas installé | Relancer Install-ADDSForest |
| Réplication échouée | Firewall bloque port 389 | Ouvrir port 389 TCP/UDP |
| Utilisateurs invisibles | Pas d'OUs créées | Créer OUs via DSA.msc |

### 7.3 Application Web

| Problème | Cause | Solution |
|---------|-------|----------|
| Page d'erreur 500 | Erreur Python | Vérifier logs : journalctl -u ymmo-app.service |
| Connexion DB échouée | MySQL pas accessible | Vérifier : sudo systemctl status mysql |
| Port 5000 occupé | Service déjà actif | Utiliser : sudo lsof -i :5000 |

### 7.4 Docker

| Problème | Cause | Solution |
|---------|-------|----------|
| Docker daemon ne démarre | Permissions insuffisantes | Ajouter user à groupe docker |
| Container crash au démarrage | Configuration YAML invalide | Vérifier docker-compose.yml avec : docker-compose config |
| Port déjà utilisé | Conflit de ports | Modifier ports dans docker-compose.yml |

---

## 8. Livrables de Déploiement

**À la fin du déploiement :**

```
Documentation :
✓ Guide-configuration-serveurs.md (ce document)
✓ Plan-adressage-IP.md
✓ Politique-securite.md
✓ Matrices-droits-acces.md
✓ Plan-sauvegarde-supervision.md
✓ Solution-cloud.md
✓ Guide-deploiement.md (ce document)

Fichiers de Configuration :
✓ Scripts PowerShell (AD, DNS)
✓ Scripts Bash (Web, Docker)
✓ Docker-compose.yml (Traefik, Uptime Kuma, Zabbix)
✓ Fichier systemd pour Flask

Infrastructure :
✓ 6 VMs opérationnelles
✓ 3 réseaux VMnet configurés
✓ Services en haute disponibilité
✓ Monitoring et alertes actifs

Tests :
✓ Tests de connectivité passés
✓ Tests de services passés
✓ RTO/RPO validés
✓ Documentation validée
```

---

**Document créé pour le projet YMMO Immobilier - Juin 2026**

**Version : 1.0**
**Dernier mise à jour : 03/06/2026**
**Auteur : Équipe INFRA B2 Ynov**

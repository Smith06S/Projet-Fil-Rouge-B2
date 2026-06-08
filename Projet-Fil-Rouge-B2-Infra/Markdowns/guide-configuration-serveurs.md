# Guide de Configuration des Serveurs - YMMO Immobilier

## 1. Configuration du Contrôleur de Domaine (DC-SIEGE)

### 1.1 Prérequis
- Windows Server 2022
- IP statique : 10.0.0.10/24
- Gateway : 10.0.0.1 (OPNSense)
- DNS : 10.0.0.1 (OPNSense)
- 4 GB RAM minimum
- 40 GB disque dur

### 1.2 Installation d'Active Directory
```powershell
# Installer le rôle AD-Domain-Services
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools

# Promouvoir en contrôleur de domaine
Install-ADDSForest -DomainName "ymmo.local" `
  -DomainNetbiosName "YMMO" `
  -InstallDns `
  -SafeModeAdministratorPassword (ConvertTo-SecureString "DSRM123!" -AsPlainText -Force) `
  -Force
```

### 1.3 Configuration du DNS
```powershell
# Ajouter les enregistrements DNS via OPNSense ou cmd
dnscmd localhost /recordadd ymmo.local ymmo A 10.0.0.11
dnscmd localhost /recordadd ymmo.local srv-web-bdd A 10.0.0.11
dnscmd localhost /recordadd ymmo.local srv-docker-monitoring A 10.0.0.12
```

### 1.4 Configuration DHCP
```powershell
# Installer le rôle DHCP
Install-WindowsFeature -Name DHCP -IncludeManagementTools

# Créer un scope DHCP pour le réseau siège
Add-DhcpServerv4Scope -Name "Siège-YMMO" `
  -StartRange 10.0.0.100 `
  -EndRange 10.0.0.130 `
  -SubnetMask 255.255.255.0
```

### 1.5 Création des Unités d'Organisation et Utilisateurs
```powershell
# Créer les OUs
New-ADOrganizationalUnit -Name "YMMO-Utilisateurs" -Path "DC=ymmo,DC=local"
New-ADOrganizationalUnit -Name "YMMO-Ordinateurs" -Path "DC=ymmo,DC=local"

# Créer les sous-OUs par département
New-ADOrganizationalUnit -Name "Direction" -Path "OU=YMMO-Utilisateurs,DC=ymmo,DC=local"
New-ADOrganizationalUnit -Name "Commercial" -Path "OU=YMMO-Utilisateurs,DC=ymmo,DC=local"
New-ADOrganizationalUnit -Name "RH-Juridique" -Path "OU=YMMO-Utilisateurs,DC=ymmo,DC=local"

# Créer les utilisateurs de test
$password = ConvertTo-SecureString "User123!" -AsPlainText -Force
New-ADUser -Name "jdirecteur" -UserPrincipalName "jdirecteur@ymmo.local" -AccountPassword $password -Enabled $true
New-ADUser -Name "mcommercial" -UserPrincipalName "mcommercial@ymmo.local" -AccountPassword $password -Enabled $true
```

### 1.6 Configuration de la Réplication AD
- Site : Default-First-Site-Name
- Réplication avec DC-SIEGE-02 (à venir)
- Fréquence : toutes les 15 minutes

---

## 2. Configuration du Serveur Web et Base de Données (SRV-WEB-BDD)

### 2.1 Prérequis
- Ubuntu 22.04 LTS
- IP statique : 10.0.0.11/24
- Gateway : 10.0.0.1
- DNS : 10.0.0.1
- 4 GB RAM minimum
- 50 GB disque dur

### 2.2 Installation d'Apache et Python
```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Apache
sudo apt install apache2 apache2-utils -y
sudo systemctl enable apache2
sudo systemctl start apache2

# Activer les modules proxy pour Flask
sudo a2enmod rewrite
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod ssl
sudo systemctl restart apache2
```

### 2.3 Installation de MySQL
```bash
# Installer MySQL Server
sudo apt install mysql-server mysql-client -y
sudo systemctl enable mysql
sudo systemctl start mysql

# Sécuriser MySQL
sudo mysql_secure_installation

# Créer la base de données YMMO
sudo mysql -u root -p << EOF
CREATE DATABASE ymmo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'ymmo_user'@'localhost' IDENTIFIED BY 'YmmoPass123!';
GRANT ALL PRIVILEGES ON ymmo_db.* TO 'ymmo_user'@'localhost';
FLUSH PRIVILEGES;
EOF
```

### 2.4 Configuration de l'Application Flask
```bash
# Installer Python et dépendances
sudo apt install python3 python3-pip python3-venv -y
sudo pip3 install flask flask-cors python-dotenv

# Copier l'application
sudo mkdir -p /var/www/html/ymmo
sudo cp -r /var/www/html/Projet-Fil-Rouge-B2_copie/* /var/www/html/ymmo/
sudo chown -R www-data:www-data /var/www/html/ymmo
```

### 2.5 Configuration du Virtual Host Apache
```apache
<VirtualHost *:80>
    ServerName ymmo.immo
    ServerAlias srv-web-bdd.ymmo.local
    DocumentRoot /var/www/html/ymmo
    
    <Directory /var/www/html/ymmo>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/ymmo-error.log
    CustomLog ${APACHE_LOG_DIR}/ymmo-access.log combined
</VirtualHost>
```

### 2.6 Création du Service Systemd pour l'Application
```ini
[Unit]
Description=YMMO Python Flask Application
After=network.target

[Service]
Type=simple
User=ymmo
Group=ymmo
WorkingDirectory=/var/www/html/ymmo
ExecStart=/usr/bin/python3 /var/www/html/ymmo/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 3. Configuration du Serveur Docker et Monitoring (SRV-DOCKER-MONITORING)

### 3.1 Prérequis
- Ubuntu 22.04 LTS
- IP statique : 10.0.0.12/24
- Gateway : 10.0.0.1
- DNS : 10.0.0.1
- 8 GB RAM minimum
- 100 GB disque dur

### 3.2 Installation de Docker
```bash
# Installer Docker
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
newgrp docker

# Installer Docker Compose
sudo apt install docker-compose -y

# Vérifier l'installation
docker --version
docker-compose --version
```

### 3.3 Configuration de Dockge
```bash
# Créer les répertoires
mkdir -p ~/docker/dockge ~/docker/stacks

# Lancer Dockge
docker run -d \
  --name dockge \
  -p 5001:5001 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/docker/dockge:/app/data \
  louislam/dockge:latest

# Accès : http://10.0.0.12:5001
# Credentials : admin / Dockge123!
```

### 3.4 Stack Traefik
```yaml
version: '3.8'
services:
  traefik:
    image: traefik:v2.11
    container_name: traefik
    restart: unless-stopped
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - traefik-net

networks:
  traefik-net:
    name: traefik-net
    driver: bridge
```

### 3.5 Stack Uptime Kuma
```yaml
version: '3.8'
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: unless-stopped
    ports:
      - "3001:3001"
    volumes:
      - ./data:/app/data
    networks:
      - traefik-net

networks:
  traefik-net:
    external: true
```

**Monitors à configurer :**
- OPNSense Firewall (10.0.0.1) - Ping
- DC-SIEGE (10.0.0.10) - Ping
- SRV-WEB-BDD (10.0.0.11) - HTTP + MySQL Port 3306
- Docker Server (localhost) - Ping

### 3.6 Stack Zabbix
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    container_name: zabbix-db
    environment:
      POSTGRES_DB: zabbix
      POSTGRES_USER: zabbix
      POSTGRES_PASSWORD: zabbix_pass
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - zabbix-net

  zabbix-server:
    image: zabbix/zabbix-server-pgsql:alpine-6.4-latest
    container_name: zabbix-server
    environment:
      DB_SERVER_HOST: postgres
      POSTGRES_DB: zabbix
      POSTGRES_USER: zabbix
      POSTGRES_PASSWORD: zabbix_pass
    depends_on:
      - postgres
    ports:
      - "10051:10051"
    networks:
      - zabbix-net

  zabbix-web:
    image: zabbix/zabbix-web-nginx-pgsql:alpine-6.4-latest
    container_name: zabbix-web
    environment:
      DB_SERVER_HOST: postgres
      POSTGRES_DB: zabbix
      POSTGRES_USER: zabbix
      POSTGRES_PASSWORD: zabbix_pass
      ZBX_SERVER_HOST: zabbix-server
    ports:
      - "8081:8080"
    depends_on:
      - postgres
      - zabbix-server
    networks:
      - zabbix-net

volumes:
  postgres-data:

networks:
  zabbix-net:
    name: zabbix-net
    driver: bridge
```

### 3.7 Installation de Zabbix Agent
```bash
sudo apt install zabbix-agent2 -y

# Configuration
sudo nano /etc/zabbix/zabbix_agent2.conf
# Server=localhost
# ServerActive=localhost:10051
# Hostname=Ubuntu-Docker

sudo systemctl enable zabbix-agent2
sudo systemctl restart zabbix-agent2
```

---

## 4. Configuration du Firewall (OPNSense)

### 4.1 Accès et Identifiants
- URL : https://10.0.0.1
- Credentials : admin / (mot de passe configuré)

### 4.2 Configuration des Interfaces
- **LAN (VMnet2)** : 10.0.0.1/24 - Réseau Siège
- **AGENCE1 (VMnet3)** : 10.1.0.1/24 - Réseau Agence Paris
- **WAN** : Accès Internet (simulé)

### 4.3 Configuration DNS Unbound
```
Services > Unbound DNS > General
- Enable Unbound : ✓
- Listen Port : 53
- Network Interfaces : LAN

Host Overrides :
- ymmo.immo → 10.0.0.11
- srv-web-bdd.ymmo.local → 10.0.0.11
- srv-docker-monitoring.ymmo.local → 10.0.0.12
- dc-siege.ymmo.local → 10.0.0.10
- nas-backup.ymmo.local → 10.0.0.20
```

### 4.4 Règles Firewall
```
LAN to LAN : Allow all
LAN to WAN : Allow all
WAN to LAN : Deny (sauf établies)
```

### 4.5 Configuration VPN IPSec (Site-à-site)
- Protocol : IKEv2
- Encryption : AES-256-GCM
- Authentification : SHA256
- DH Group : 14
- PSK : YmmoSecureVPN2024!

---

## 5. Checklist de Vérification

### Après chaque démarrage
- [ ] OPNSense accessible (https://10.0.0.1)
- [ ] DC-SIEGE ping répond
- [ ] SRV-WEB-BDD ping répond et site accessible
- [ ] SRV-DOCKER-MONITORING ping répond
- [ ] Dockge accessible (http://10.0.0.12:5001)
- [ ] Traefik accessible (http://10.0.0.12:8080)
- [ ] Uptime Kuma accessible (http://10.0.0.12:3001)
- [ ] Zabbix accessible (http://10.0.0.12:8081)
- [ ] DNS résout ymmo.immo → 10.0.0.11

### Services à vérifier
```bash
# Sur DC-SIEGE
dcdiag /v
nltest /dclist:ymmo.local

# Sur SRV-WEB-BDD
sudo systemctl status apache2
sudo systemctl status mysql
sudo systemctl status ymmo-app.service

# Sur SRV-DOCKER-MONITORING
docker ps
docker compose ps -a
sudo systemctl status zabbix-agent2
```

---

## 6. Troubleshooting

### Problème : DC-SIEGE ne résout pas les noms
**Solution :** Configurer le DNS d'OPNSense comme primaire

### Problème : Application Flask ne démarre pas
**Solution :** Vérifier les logs : `sudo journalctl -u ymmo-app.service -f`

### Problème : Zabbix n'affiche pas les métriques
**Solution :** Redémarrer l'agent : `sudo systemctl restart zabbix-agent2`

### Problème : Traefik n'affiche pas les services
**Solution :** Vérifier Docker socket : `ls -la /var/run/docker.sock`

---

**Document créé pour le projet YMMO Immobilier - Juin 2026**

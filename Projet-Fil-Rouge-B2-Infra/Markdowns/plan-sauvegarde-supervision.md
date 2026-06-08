# Plan de Sauvegarde et Supervision - YMMO Immobilier

## 1. Stratégie de Sauvegarde

### 1.1 Objectifs de Sauvegarde
- **RPO (Recovery Point Objective)** : 24 heures
- **RTO (Recovery Time Objective)** : 4 heures
- **Rétention** : 30 jours minimum

### 1.2 Données Critiques à Sauvegarder

#### Données du Contrôleur de Domaine (DC-SIEGE)
```
Localisation : C:\Windows\ntds\ntds.dit (Active Directory)
Fréquence : Quotidienne (23h00)
Destination : NAS Synology (10.0.0.20)
Rétention : 30 jours
```

#### Base de Données YMMO (SRV-WEB-BDD)
```
Localisation : /var/lib/mysql/ymmo_db
Fréquence : Quotidienne (22h30)
Destination : NAS Synology (10.0.0.20)
Rétention : 30 jours
Méthode : mysqldump + compression gzip
```

#### Dossier Applicatif Web
```
Localisation : /var/www/html/ymmo
Fréquence : Quotidienne (22h00)
Destination : NAS Synology (10.0.0.20)
Rétention : 7 jours (sauvegardes incrémentielles)
```

#### Configurations Docker
```
Localisation : ~/docker/stacks (docker-compose.yml)
Fréquence : À chaque modification
Destination : NAS Synology (10.0.0.20) + GitHub
Rétention : Illimité (versionné sur Git)
```

### 1.3 Calendrier de Sauvegarde

| Jour | Heure | Élément | Durée estimée |
|------|-------|--------|---------------|
| Lun-Dim | 22:00 | Application Web | 10 min |
| Lun-Dim | 22:30 | Base de données MySQL | 20 min |
| Lun-Dim | 23:00 | Active Directory | 15 min |
| Samedi | 12:00 | Sauvegarde complète | 1 heure |

### 1.4 Procédure de Sauvegarde MySQL

```bash
#!/bin/bash
# Script de sauvegarde quotidienne MySQL

BACKUP_DIR="/mnt/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
DB_USER="ymmo_user"
DB_PASSWORD="YmmoPass123!"

# Créer le répertoire de sauvegarde
mkdir -p $BACKUP_DIR

# Sauvegarder les bases de données
mysqldump -u $DB_USER -p$DB_PASSWORD \
  --all-databases \
  --single-transaction \
  --quick \
  --lock-tables=false | gzip > $BACKUP_DIR/ymmo_db_$DATE.sql.gz

# Supprimer les sauvegardes de plus de 30 jours
find $BACKUP_DIR -name "ymmo_db_*.sql.gz" -mtime +30 -delete

# Vérifier la sauvegarde
if [ -f "$BACKUP_DIR/ymmo_db_$DATE.sql.gz" ]; then
    echo "[OK] Sauvegarde MySQL réussie - $DATE"
else
    echo "[ERREUR] Sauvegarde MySQL échouée - $DATE"
fi
```

**Installation via cron :**
```bash
# Ajouter au crontab root
sudo crontab -e

# Ajouter la ligne :
30 22 * * * /usr/local/bin/backup-mysql.sh >> /var/log/backup-mysql.log 2>&1
```

### 1.5 Procédure de Sauvegarde Active Directory

```powershell
# Script PowerShell de sauvegarde AD
$BackupPath = "\\10.0.0.20\backups\AD"
$Date = Get-Date -Format "yyyyMMdd_HHmmss"

# Créer un snapshot VSS
wbadmin start backup -backupTarget:$BackupPath -systemState -quiet

# Sauvegarder la base AD
ntdsutil "ac i ntds" "ifm" "create full D:\AD_Backup" quit quit

# Supprimer les sauvegardes de plus de 30 jours
Get-ChildItem $BackupPath -Filter "*" | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item -Force
```

**Planification via Tâches planifiées Windows :**
```
Nom : Sauvegarde Active Directory
Fréquence : Quotidienne à 23:00
Action : powershell.exe -File C:\Scripts\Backup-AD.ps1
```

### 1.6 Restauration à partir d'une Sauvegarde

#### Restaurer MySQL
```bash
# Vérifier les sauvegardes disponibles
ls -lh /mnt/backup/mysql/

# Restaurer une sauvegarde
gunzip < /mnt/backup/mysql/ymmo_db_20260603_220000.sql.gz | mysql -u root -p

# Vérifier la restauration
mysql -u ymmo_user -p ymmo_db -e "SELECT COUNT(*) FROM tables;"
```

#### Restaurer Active Directory
```powershell
# Restaurer depuis une sauvegarde VSS
wbadmin start recovery -version:06/03/2026-23:00 -itemType:Volume -items:C: -recoveryTarget:C:

# Ou restaurer la base NTDS
ntdsutil "ac i ntds" "ifm" "restore D:\AD_Backup" quit quit
dcdiag /v  # Vérifier l'intégrité
```

---

## 2. Plan de Supervision

### 2.1 Outils de Supervision Déployés

#### Uptime Kuma (Monitoring Basique)
```
URL : http://10.0.0.12:3001
Credentials : admin / Kuma123!
Rôle : Monitoring de disponibilité (ping, HTTP)
```

#### Zabbix (Monitoring Avancé)
```
URL : http://10.0.0.12:8081
Credentials : Admin / zabbix
Rôle : Monitoring CPU, RAM, Disque, Logs
```

### 2.2 Monitors Uptime Kuma Configurés

| Nom | Type | Cible | Intervalle | Seuil |
|-----|------|-------|-----------|-------|
| OPNSense Firewall | Ping | 10.0.0.1 | 60s | 3 retry |
| DC-SIEGE | Ping | 10.0.0.10 | 60s | 3 retry |
| SRV-WEB-BDD HTTP | HTTP | http://10.0.0.11 | 120s | 3 retry |
| SRV-WEB-BDD MySQL | Port | 10.0.0.11:3306 | 120s | 3 retry |
| SRV-Docker-Monitoring | Ping | 10.0.0.12 | 60s | 3 retry |

### 2.3 Métriques Zabbix Supervisées

#### Serveur DC-SIEGE
```
- CPU Utilization (%)
- Memory Utilization (%)
- Disk Free Space (C:)
- Network Traffic (In/Out)
- Active Directory Replication Status
- DNS Query Count
- NTDS Database Size
```

#### Serveur SRV-WEB-BDD
```
- CPU Utilization (%)
- Memory Utilization (%)
- Disk Free Space
- Network Traffic
- Apache Status (active connections)
- MySQL Process Memory
- Database Query Latency
- Flask Application Response Time
```

#### Serveur SRV-Docker-Monitoring
```
- CPU Utilization (%)
- Memory Utilization (%)
- Disk Free Space
- Docker Container Count
- Docker Memory Usage
- Network Traffic
- Zabbix Agent Status
```

#### Firewall OPNSense
```
- CPU Temperature
- Memory Usage
- Network Traffic (LAN/WAN)
- VPN Connection Status
- Firewall Rules Statistics
- DNS Queries Processed
```

### 2.4 Alertes Configurées

#### Seuils Critiques
```
CPU Utilization > 85% → Alert CRITICAL
Memory Utilization > 90% → Alert CRITICAL
Disk Free Space < 10% → Alert CRITICAL
MySQL Service Down → Alert CRITICAL
AD Replication Failed → Alert CRITICAL
```

#### Seuils Avertissements
```
CPU Utilization > 70% → Alert WARNING
Memory Utilization > 75% → Alert WARNING
Disk Free Space < 20% → Alert WARNING
Service Response Time > 2s → Alert WARNING
```

### 2.5 Configuration des Notifications

#### Email (SMTP)
```
Serveur : mail.ymmo.local (à configurer)
Port : 587
Utilisateur : alertes@ymmo.local
De : Zabbix Alertes <alertes@ymmo.local>
À : administrateurs@ymmo.local
```

#### Webhook Slack (optionnel)
```
URL : https://hooks.slack.com/services/YOUR/WEBHOOK/URL
Canal : #infrastructure-alerts
```

### 2.6 Dashboards de Supervision

#### Dashboard Zabbix - Vue Générale
```
Layout :
- État global des serveurs (4 carrés)
- Graphiques CPU/Memory/Disk (temps réel)
- Événements critiques récents
- État de chaque service (AD, MySQL, Docker)
```

#### Dashboard Uptime Kuma - Résumé
```
- Disponibilité 24h (en %)
- Ping moyen (ms)
- Statut de chaque monitor (✓/✗)
- Graphique de disponibilité (30 jours)
```

### 2.7 Rapports Périodiques

#### Rapport Hebdomadaire
```
Jour : Chaque lundi 08:00
Contenu :
- Disponibilité moyenne (%)
- Incidents détectés
- Performance (latence moyenne)
- Recommandations
```

#### Rapport Mensuel
```
Jour : 1er du mois à 09:00
Contenu :
- Statistiques mensuelles
- Analyse des tendances
- Alertes par sévérité
- Capacité restante
- Recommandations optimisation
```

---

## 3. Procédures de Maintenance

### 3.1 Maintenance Préventive

#### Hebdomadaire
```
- [ ] Vérifier les logs des sauvegardes
- [ ] Vérifier la réplication AD (repadmin)
- [ ] Vérifier l'espace disque NAS
- [ ] Vérifier les alertes Zabbix en attente
```

#### Mensuelle
```
- [ ] Test de restauration d'une sauvegarde
- [ ] Vérifier les certificats SSL expiration
- [ ] Nettoyer les logs (> 30 jours)
- [ ] Vérifier les mises à jour disponibles
- [ ] Audit des accès AD (Last Logon)
```

#### Trimestrielle
```
- [ ] Audit complet de sécurité
- [ ] Test de basculement en cas de sinistre
- [ ] Vérifier la capacité disque (tendances)
- [ ] Optimisation des performances
```

### 3.2 Maintenance Corrective

#### Procédure Incident CRITIQUE
```
1. Identifier le service affecté
2. Consulter les logs (Zabbix, Uptime Kuma)
3. Redémarrer le service
4. Vérifier la restauration
5. Documenter l'incident
6. Analyser la cause racine
```

#### Escalade
```
Niveau 1 : Support Technique (1h max)
Niveau 2 : Chef Projet INFRA (2h max)
Niveau 3 : Administrateur Principal (permanent)
```

---

## 4. Métriques de Performance

### 4.1 Objectifs de Disponibilité

| Composant | SLA | Métrique |
|-----------|-----|----------|
| Active Directory | 99.9% | 43 min/mois |
| Site Web | 99.5% | 3h36/mois |
| Base de Données | 99.9% | 43 min/mois |
| Infrastructure | 99.5% | 3h36/mois |

### 4.2 Métriques Clés (KPI)

```
MTBF (Mean Time Between Failures) : > 720 heures
MTTR (Mean Time To Repair) : < 30 minutes
RTO (Recovery Time Objective) : 4 heures
RPO (Recovery Point Objective) : 24 heures
Disponibilité mensuelle : > 99.5%
Temps de réponse moyen : < 500ms
Taux d'erreur : < 0.1%
```

### 4.3 Rapports de Performance

**Graphiques mensuels :**
- Disponibilité par service (%)
- Temps de réponse (ms)
- Utilisation CPU/RAM/Disque (%)
- Nombre d'incidents
- MTTR par incident

---

## 5. Plan de Continuité de Service

### 5.1 Procédure de Basculement (Failover)

#### Scénario : Perte de DC-SIEGE
```
1. Promouvoir DC-SIEGE-02 en DC principal
   Install-ADDSDomainController -DomainName "ymmo.local" -Credential (Get-Credential)

2. Mettre à jour les enregistrements DNS
   dnscmd localhost /recordmod ymmo.local dc-siege A 10.0.0.13

3. Vérifier la réplication AD
   repadmin /showrepl

4. Tester l'accès au domaine
   nltest /dsgetsite
```

#### Scénario : Perte de SRV-WEB-BDD
```
1. Restaurer la dernière sauvegarde sur une VM de remplacement
   gunzip < backup.sql.gz | mysql -u root -p

2. Vérifier la base de données
   mysql -u ymmo_user -p ymmo_db -e "SELECT COUNT(*) FROM users;"

3. Redémarrer les services
   sudo systemctl restart apache2
   sudo systemctl restart mysql
   sudo systemctl restart ymmo-app.service

4. Tester l'accès au site
   curl http://ymmo.immo
```

### 5.2 Procédure de Restauration

**Étapes générales :**
1. Préparer la VM de remplacement
2. Installer l'OS et les services de base
3. Restaurer les données depuis la sauvegarde
4. Vérifier l'intégrité des données
5. Tester les fonctionnalités critiques
6. Basculer le service (DNS, adresses IP)

---

**Document créé pour le projet YMMO Immobilier - Juin 2026**

# MATRICE DES DROITS D'ACCÈS - INFRASTRUCTURE YMMO

**Projet :** Infrastructure YMMO  
**Version :** 1.0  
**Date :** Février 2026

---

## 1. PRINCIPES GÉNÉRAUX

### 1.1 Philosophie de sécurité
- **Moindre privilège :** Chaque utilisateur/groupe dispose uniquement des droits nécessaires à ses fonctions
- **Séparation des responsabilités :** Les rôles critiques sont séparés
- **Traçabilité :** Tous les accès sont journalisés
- **Révision régulière :** Révision trimestrielle des droits d'accès

### 1.2 Légende
- **L (Lecture) :** Consultation uniquement, pas de modification
- **E (Écriture) :** Création et modification de fichiers
- **S (Suppression) :** Suppression de fichiers et dossiers
- **M (Modification) :** Modification des permissions et propriétés
- **C (Contrôle total) :** Tous les droits y compris gestion des permissions
- **- (Aucun) :** Aucun accès
- **I (Interdit) :** Accès explicitement refusé

---

## 2. MATRICE DES DROITS - PARTAGES RÉSEAU

### 2.1 Partages départementaux (Serveur DC-SIEGE)

| Dossier partagé | Direction | Commercial | Communication<br/>Marketing | RH<br/>Juridique | IT<br/>Support |
|-----------------|-----------|------------|------------------------------|------------------|----------------|
| **\\DC-SIEGE\Direction** | **L+E+S** | L | L | L | L |
| **\\DC-SIEGE\Commercial** | **L+E+S** | **L+E+S** | L | L | L |
| **\\DC-SIEGE\Marketing** | **L+E+S** | L | **L+E+S** | L | L |
| **\\DC-SIEGE\RH-Juridique** | **L+E+S** | L | L | **L+E+S** | L |
| **\\DC-SIEGE\IT-Support** | **L+E+S** | L | L | L | **L+E+S** |

**Détails des permissions NTFS :**

#### Partage : Direction
- **Path :** C:\Partages\Direction
- **Permissions partage :**
  - GRP-Direction : Full Control
  - Everyone : Read
- **Permissions NTFS :**
  - GRP-Direction : Modify, Read & Execute, List Folder Contents, Read, Write
  - GRP-Commercial : Read & Execute, List Folder Contents, Read
  - GRP-Communication-Marketing : Read & Execute, List Folder Contents, Read
  - GRP-RH-Juridique : Read & Execute, List Folder Contents, Read
  - GRP-IT-Support : Read & Execute, List Folder Contents, Read
  - SYSTEM : Full Control
  - Administrators : Full Control

#### Partage : Commercial
- **Path :** C:\Partages\Commercial
- **Permissions partage :**
  - GRP-Direction : Full Control
  - GRP-Commercial : Change
  - Everyone : Read
- **Permissions NTFS :**
  - GRP-Direction : Modify, Read & Execute, List Folder Contents, Read, Write
  - GRP-Commercial : Modify, Read & Execute, List Folder Contents, Read, Write
  - GRP-Communication-Marketing : Read & Execute, List Folder Contents, Read
  - GRP-RH-Juridique : Read & Execute, List Folder Contents, Read
  - GRP-IT-Support : Read & Execute, List Folder Contents, Read
  - SYSTEM : Full Control
  - Administrators : Full Control

#### Partage : Marketing
- **Path :** C:\Partages\Marketing
- **Permissions partage :**
  - GRP-Direction : Full Control
  - GRP-Communication-Marketing : Change
  - Everyone : Read
- **Permissions NTFS :**
  - GRP-Direction : Modify, Read & Execute, List Folder Contents, Read, Write
  - GRP-Communication-Marketing : Modify, Read & Execute, List Folder Contents, Read, Write
  - GRP-Commercial : Read & Execute, List Folder Contents, Read
  - GRP-RH-Juridique : Read & Execute, List Folder Contents, Read
  - GRP-IT-Support : Read & Execute, List Folder Contents, Read
  - SYSTEM : Full Control
  - Administrators : Full Control

#### Partage : RH-Juridique
- **Path :** C:\Partages\RH-Juridique
- **Permissions partage :**
  - GRP-Direction : Full Control
  - GRP-RH-Juridique : Change
  - Everyone : Read
- **Permissions NTFS :**
  - GRP-Direction : Modify, Read & Execute, List Folder Contents, Read, Write
  - GRP-RH-Juridique : Modify, Read & Execute, List Folder Contents, Read, Write
  - GRP-Commercial : Read & Execute, List Folder Contents, Read
  - GRP-Communication-Marketing : Read & Execute, List Folder Contents, Read
  - GRP-IT-Support : Read & Execute, List Folder Contents, Read
  - SYSTEM : Full Control
  - Administrators : Full Control

#### Partage : IT-Support
- **Path :** C:\Partages\IT-Support
- **Permissions partage :**
  - GRP-Direction : Full Control
  - GRP-IT-Support : Change
  - Everyone : Read
- **Permissions NTFS :**
  - GRP-Direction : Modify, Read & Execute, List Folder Contents, Read, Write
  - GRP-IT-Support : Modify, Read & Execute, List Folder Contents, Read, Write
  - GRP-Commercial : Read & Execute, List Folder Contents, Read
  - GRP-Communication-Marketing : Read & Execute, List Folder Contents, Read
  - GRP-RH-Juridique : Read & Execute, List Folder Contents, Read
  - SYSTEM : Full Control
  - Administrators : Full Control

---

### 2.2 Partages Samba (Serveur SRV-WEB-BDD)

| Dossier partagé | Direction | Commercial | Communication<br/>Marketing | RH<br/>Juridique | IT<br/>Support |
|-----------------|-----------|------------|------------------------------|------------------|----------------|
| **\\SRV-WEB-BDD\Documents-YMMO** | L+E+S | L+E+S | L+E+S | L+E+S | L+E+S |
| **\\SRV-WEB-BDD\Uploads-Web** | L | L | L+E+S | L | C |

**Configuration Samba (smb.conf) :**

#### Partage : Documents-YMMO
```ini
[Documents-YMMO]
   path = /srv/samba/documents-ymmo
   browseable = yes
   read only = no
   valid users = @ymmo-users
   create mask = 0775
   directory mask = 0775
   force user = nobody
   force group = nogroup
```

#### Partage : Uploads-Web
```ini
[Uploads-Web]
   path = /var/www/html/ymmo/uploads
   browseable = yes
   read only = no
   valid users = @ymmo-marketing, @ymmo-it
   write list = @ymmo-marketing, @ymmo-it
   create mask = 0664
   directory mask = 0775
   force user = www-data
   force group = www-data
```

---

## 3. MATRICE DES DROITS - SERVICES RÉSEAU

### 3.1 Active Directory

| Service / Fonction | Direction | Commercial | Communication<br/>Marketing | RH<br/>Juridique | IT<br/>Support |
|--------------------|-----------|------------|------------------------------|------------------|----------------|
| **Connexion au domaine** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Modifier son mot de passe** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Joindre un PC au domaine** | - | - | - | - | ✓ |
| **Créer des utilisateurs** | - | - | - | - | ✓ |
| **Modifier les utilisateurs** | - | - | - | Limité (RH) | ✓ |
| **Réinitialiser mots de passe** | - | - | - | Limité (RH) | ✓ |
| **Créer des groupes** | - | - | - | - | ✓ |
| **Modifier GPO** | - | - | - | - | ✓ |
| **Accès console serveur** | - | - | - | - | ✓ |

**Délégation AD :**
- **GRP-IT-Support :** Membre de "Domain Admins" - Droits complets
- **GRP-RH-Juridique :** Délégation sur OU "YMMO-Utilisateurs" pour :
  - Réinitialiser les mots de passe
  - Lire toutes les informations utilisateur
  - Modifier les propriétés utilisateur (téléphone, bureau, etc.)

---

### 3.2 Application Web

| Fonctionnalité | Direction | Commercial | Communication<br/>Marketing | RH<br/>Juridique | IT<br/>Support |
|----------------|-----------|------------|------------------------------|------------------|----------------|
| **Connexion à l'application** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Consulter les biens** | ✓ | ✓ | ✓ | - | ✓ |
| **Ajouter un bien** | ✓ | ✓ | - | - | ✓ |
| **Modifier un bien** | ✓ | ✓ | - | - | ✓ |
| **Supprimer un bien** | ✓ | - | - | - | ✓ |
| **Consulter les clients** | ✓ | ✓ | ✓ | - | ✓ |
| **Ajouter un client** | ✓ | ✓ | - | - | ✓ |
| **Modifier un client** | ✓ | ✓ | - | - | ✓ |
| **Consulter les transactions** | ✓ | ✓ | - | - | ✓ |
| **Créer une transaction** | ✓ | ✓ | - | - | ✓ |
| **Valider une transaction** | ✓ | - | - | - | - |
| **Annuler une transaction** | ✓ | - | - | - | ✓ |
| **Tableau de bord statistiques** | ✓ | ✓ | ✓ | - | ✓ |
| **Export de données** | ✓ | - | - | - | ✓ |
| **Gestion des utilisateurs app** | - | - | - | - | ✓ |
| **Accès aux logs** | - | - | - | - | ✓ |
| **Configuration application** | - | - | - | - | ✓ |

**Rôles dans la base de données :**
```sql
-- Rôles MySQL pour ymmo_db
CREATE ROLE 'role_direction';
CREATE ROLE 'role_commercial';
CREATE ROLE 'role_marketing';
CREATE ROLE 'role_rh';
CREATE ROLE 'role_it';

-- Permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ymmo_db.* TO 'role_direction';
GRANT SELECT, INSERT, UPDATE ON ymmo_db.biens_immobiliers TO 'role_commercial';
GRANT SELECT, INSERT, UPDATE ON ymmo_db.clients TO 'role_commercial';
GRANT SELECT ON ymmo_db.* TO 'role_marketing';
GRANT SELECT ON ymmo_db.utilisateurs TO 'role_rh';
GRANT ALL PRIVILEGES ON ymmo_db.* TO 'role_it';
```

---

### 3.3 Services de monitoring

| Service | Direction | Commercial | Communication<br/>Marketing | RH<br/>Juridique | IT<br/>Support |
|---------|-----------|------------|------------------------------|------------------|----------------|
| **Uptime Kuma (consultation)** | ✓ | - | - | - | ✓ |
| **Uptime Kuma (configuration)** | - | - | - | - | ✓ |
| **Zabbix (consultation)** | ✓ | - | - | - | ✓ |
| **Zabbix (configuration)** | - | - | - | - | ✓ |
| **Dockge (consultation)** | - | - | - | - | ✓ |
| **Dockge (gestion stacks)** | - | - | - | - | ✓ |
| **Traefik Dashboard** | - | - | - | - | ✓ |

---

### 3.4 Firewall OPNSense

| Accès / Fonction | Direction | Commercial | Communication<br/>Marketing | RH<br/>Juridique | IT<br/>Support |
|------------------|-----------|------------|------------------------------|------------------|----------------|
| **Interface Web OPNSense** | - | - | - | - | ✓ |
| **Consultation logs** | - | - | - | - | ✓ |
| **Modification règles** | - | - | - | - | ✓ |
| **Configuration VPN** | - | - | - | - | ✓ |
| **Gestion utilisateurs** | - | - | - | - | ✓ |
| **Console système** | - | - | - | - | ✓ |

**Comptes OPNSense :**
- **root :** Compte administrateur principal (IT Support uniquement)
- **admin-it :** Compte administrateur secondaire (IT Support)
- **viewer :** Compte consultation seule (Direction sur demande)

---

## 4. MATRICE DES DROITS - INFRASTRUCTURE

### 4.1 Accès aux serveurs

| Serveur | Direction | Commercial | Communication<br/>Marketing | RH<br/>Juridique | IT<br/>Support |
|---------|-----------|------------|------------------------------|------------------|----------------|
| **DC-SIEGE (RDP)** | - | - | - | - | ✓ |
| **SRV-WEB-BDD (SSH)** | - | - | - | - | ✓ |
| **SRV-DOCKER (SSH)** | - | - | - | - | ✓ |
| **NAS-BACKUP (Web)** | - | - | - | - | ✓ |
| **Firewall Siège (Web)** | - | - | - | - | ✓ |
| **Firewall Agences (Web)** | - | - | - | - | ✓ |

**Comptes serveurs :**

**DC-SIEGE :**
- Administrateur local : IT Support
- YMMO\tadmin : IT Support (Domain Admin)
- YMMO\Administrateur : IT Support

**Serveurs Linux (SSH) :**
- root : Interdit (connexion désactivée)
- ymmo : Compte avec sudo (IT Support uniquement)
- backup-user : Compte de service pour sauvegardes (pas de shell)

---

### 4.2 Accès aux équipements réseau

| Équipement | Direction | Commercial | Communication<br/>Marketing | RH<br/>Juridique | IT<br/>Support |
|------------|-----------|------------|------------------------------|------------------|----------------|
| **Switch Core** | - | - | - | - | ✓ |
| **Switches Agences** | - | - | - | - | ✓ |
| **Points d'accès WiFi** | - | - | - | - | ✓ |
| **Imprimantes réseau** | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## 5. MATRICE DES DROITS - ACCÈS VPN

### 5.1 VPN IPSec Site-à-Site

| Connexion | Direction | Commercial | Communication<br/>Marketing | RH<br/>Juridique | IT<br/>Support |
|-----------|-----------|------------|------------------------------|------------------|----------------|
| **Agence → Siège** | Auto | Auto | Auto | Auto | Auto |
| **Siège → Agence** | Auto | Auto | Auto | Auto | Auto |

**Note :** Les tunnels VPN IPSec sont transparents pour les utilisateurs. L'accès aux ressources dépend des droits définis précédemment.

---

### 5.2 VPN Tailscale (Accès distant administratif)

| Utilisation | Direction | Commercial | Communication<br/>Marketing | RH<br/>Juridique | IT<br/>Support |
|-------------|-----------|------------|------------------------------|------------------|----------------|
| **Connexion Tailscale** | Sur demande | - | - | - | ✓ |
| **Accès infrastructure** | Consultation | - | - | - | ✓ |
| **Administration distante** | - | - | - | - | ✓ |

**Appareils autorisés Tailscale :**
- Laptop IT Support 1
- Laptop IT Support 2
- Laptop Direction (consultation uniquement)
- PC maison (pour démo/LAB)

---

## 6. MATRICE DES DROITS - BASE DE DONNÉES

### 6.1 Accès MySQL (ymmo_db)

| Table | Direction | Commercial | Communication<br/>Marketing | RH<br/>Juridique | IT<br/>Support |
|-------|-----------|------------|------------------------------|------------------|----------------|
| **utilisateurs** | SELECT | SELECT | SELECT | SELECT, UPDATE | ALL |
| **biens_immobiliers** | ALL | SELECT, INSERT, UPDATE | SELECT | - | ALL |
| **transactions** | ALL | SELECT, INSERT, UPDATE | SELECT | - | ALL |
| **clients** | ALL | SELECT, INSERT, UPDATE | SELECT | - | ALL |
| **agents_immobiliers** | SELECT, UPDATE | SELECT | SELECT | SELECT, UPDATE | ALL |
| **agences** | SELECT | SELECT | SELECT | - | ALL |
| **rendez_vous** | ALL | SELECT, INSERT, UPDATE, DELETE | SELECT | - | ALL |
| **documents** | ALL | SELECT, INSERT | SELECT | - | ALL |
| **logs_activite** | SELECT | - | - | - | ALL |

---

## 7. PROCÉDURES DE GESTION DES DROITS

### 7.1 Demande de droits supplémentaires

**Processus :**
1. Utilisateur fait une demande écrite (email) à son manager
2. Manager valide et transmet à IT Support
3. IT Support analyse la demande (principe du moindre privilège)
4. IT Support applique les modifications si justifié
5. IT Support notifie l'utilisateur et archive la demande

**Délai de traitement :** 48h ouvrées

---

### 7.2 Révocation de droits

**Départ d'un employé :**
1. RH notifie IT Support
2. IT Support désactive le compte AD immédiatement
3. IT Support révoque tous les accès distants
4. IT Support supprime le compte après 30 jours (archivage des données)
5. Responsable hiérarchique récupère les données si nécessaire

**Changement de poste :**
1. RH notifie IT Support
2. IT Support modifie les groupes AD selon le nouveau poste
3. Les permissions sont automatiquement ajustées via les groupes
4. IT Support vérifie que les droits sont corrects

---

### 7.3 Audit des droits

**Fréquence :** Trimestrielle

**Processus :**
1. IT Support génère un rapport des permissions
2. Chaque manager vérifie les droits de son équipe
3. Demandes de modifications si nécessaire
4. IT Support applique les corrections
5. Rapport d'audit archivé

---

## 8. JOURNALISATION ET TRAÇABILITÉ

### 8.1 Événements journalisés

**Active Directory :**
- Connexions réussies et échouées
- Modifications de comptes
- Modifications de groupes
- Modifications de GPO
- Élévation de privilèges

**Serveurs de fichiers :**
- Accès aux partages sensibles (Direction, RH)
- Modifications de permissions
- Suppressions de fichiers

**Application Web :**
- Connexions utilisateurs
- Actions critiques (création/suppression de biens, transactions)
- Modifications de configuration
- Export de données

**Firewall :**
- Connexions VPN
- Règles déclenchées
- Modifications de configuration

### 8.2 Rétention des logs

- **Logs Active Directory :** 12 mois
- **Logs serveurs :** 6 mois
- **Logs applicatifs :** 12 mois
- **Logs firewall :** 3 mois
- **Logs d'audit :** 5 ans

---

## 9. CONFORMITÉ RGPD

### 9.1 Données personnelles

**Données traitées :**
- Identité (nom, prénom)
- Coordonnées (email, téléphone)
- Données RH (salaire, contrat - RH uniquement)
- Logs de connexion

**Accès aux données personnelles :**
- RH-Juridique : Données RH complètes
- IT-Support : Données techniques uniquement (logs, comptes)
- Autres : Données professionnelles limitées

**Droits des utilisateurs :**
- Droit d'accès : Demande à RH
- Droit de rectification : Via RH ou IT selon la donnée
- Droit à l'effacement : 30 jours après départ de l'entreprise

---

## 10. CONTACTS

**Demande de droits :** it-support@ymmo.local  
**Questions RH :** rh@ymmo.local  
**Urgence sécurité :** security@ymmo.local (IT Support)

---

**Responsable :** Équipe IT Support YMMO  
**Approbation :** Direction YMMO  
**Version :** 1.0  
**Date :** Février 2026  
**Prochaine révision :** Mai 2026

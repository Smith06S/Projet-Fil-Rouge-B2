# POLITIQUE DE SÉCURITÉ - INFRASTRUCTURE YMMO

**Projet :** Infrastructure YMMO  
**Version :** 1.0  
**Date :** Février 2026  
**Statut :** En vigueur

---

## 1. INTRODUCTION

### 1.1 Objectif
Ce document définit la politique de sécurité informatique de l'entreprise YMMO. Elle vise à protéger les systèmes d'information, les données et les ressources contre les menaces internes et externes.

### 1.2 Portée
Cette politique s'applique à :
- Tous les employés de YMMO (siège et agences)
- Tous les systèmes informatiques de l'entreprise
- Tous les prestataires et partenaires ayant accès au SI

### 1.3 Responsabilités
- **Direction :** Validation et financement de la politique de sécurité
- **IT Support :** Mise en œuvre et maintien de la sécurité
- **Managers :** Application de la politique dans leurs équipes
- **Utilisateurs :** Respect des règles de sécurité

---

## 2. POLITIQUE D'AUTHENTIFICATION

### 2.1 Gestion des mots de passe

#### Exigences de complexité (Appliquée via GPO)
- **Longueur minimale :** 8 caractères
- **Complexité requise :** Oui
  - Au moins 1 majuscule (A-Z)
  - Au moins 1 minuscule (a-z)
  - Au moins 1 chiffre (0-9)
  - Au moins 1 caractère spécial (!@#$%^&*)
- **Durée de vie maximale :** 90 jours
- **Durée de vie minimale :** 1 jour
- **Historique :** 5 mots de passe mémorisés (pas de réutilisation)
- **Tentatives de connexion :** 5 maximum avant verrouillage
- **Durée de verrouillage :** 30 minutes

#### Bonnes pratiques
✅ **À FAIRE :**
- Utiliser un mot de passe unique pour chaque service
- Changer le mot de passe immédiatement en cas de suspicion de compromission
- Utiliser un gestionnaire de mots de passe (recommandé)
- Ne jamais partager son mot de passe

❌ **À NE PAS FAIRE :**
- Utiliser des informations personnelles (date de naissance, prénom, etc.)
- Écrire le mot de passe sur papier ou fichier non chiffré
- Utiliser le même mot de passe que sur des sites personnels
- Partager son mot de passe avec des collègues

#### Exemples
- ✅ **Bon :** `Ymmo2026!Secure` ou `Mon-Chat-Est-Noir-42!`
- ❌ **Mauvais :** `password`, `123456`, `ymmo`, `JeanDupont`

---

### 2.2 Authentification multi-facteurs (MFA)

**Obligatoire pour :**
- Accès VPN distant (Tailscale)
- Accès administrateur aux serveurs
- Accès au NAS de sauvegarde
- Accès à l'application web depuis l'extérieur (futur)

**Méthodes acceptées :**
- Application d'authentification (Microsoft Authenticator, Google Authenticator)
- SMS (moins sécurisé, à éviter si possible)
- Clé de sécurité matérielle (YubiKey)

---

### 2.3 Gestion des comptes

#### Création de compte
- Demande formelle de RH avec validation du manager
- Application du principe du moindre privilège
- Attribution aux groupes AD appropriés
- Formation de l'utilisateur aux règles de sécurité

#### Désactivation de compte
- **Départ définitif :** Désactivation immédiate dès notification RH
- **Absence longue durée (> 30 jours) :** Désactivation temporaire
- **Suspicion de compromission :** Désactivation immédiate + investigation

#### Suppression de compte
- **Délai :** 30 jours après désactivation
- **Archivage :** Sauvegarde des données utilisateur avant suppression
- **Transfert :** Données transférées au manager si nécessaire

---

## 3. POLITIQUE D'ACCÈS RÉSEAU

### 3.1 Sécurité périmétrique

#### Firewall OPNSense
**Configuration :**
- Politique par défaut : **DENY ALL** (tout bloquer)
- Autorisation explicite uniquement pour le trafic légitime
- Révision trimestrielle des règles
- Journalisation de toutes les connexions bloquées

**Règles de base :**
```
LAN → WAN : Autoriser (avec NAT)
LAN → LAN : Autoriser services spécifiques uniquement
WAN → LAN : Bloquer par défaut
IPSec → LAN : Autoriser trafic inter-sites
```

#### Segmentation réseau
- **Réseau siège :** 10.0.0.0/24 (infrastructure critique)
- **Réseaux agences :** 10.1.0.0/24 - 10.12.0.0/24 (sites distants)
- **Réseau VPN Management :** 172.16.0.0/24 (gestion VPN)

**Isolation :**
- Les agences n'ont pas d'accès direct entre elles (transit par le siège)
- Serveurs isolés des postes de travail (règles firewall)

---

### 3.2 VPN et accès distant

#### VPN IPSec Site-à-Site
**Sécurité :**
- Protocole : IKEv2 (recommandé par l'ANSSI)
- Chiffrement : AES-256-GCM
- Authentification : SHA-256
- Perfect Forward Secrecy (PFS) : DH Group 14 minimum
- Renouvellement des clés : Toutes les heures (Phase 2)

**Gestion des PSK (Pre-Shared Keys) :**
- Longueur minimum : 32 caractères
- Complexité élevée (majuscules, minuscules, chiffres, symboles)
- Stockage sécurisé (coffre-fort de mots de passe)
- Changement : Annuel ou en cas de compromission suspectée
- Un PSK unique par tunnel (pas de réutilisation)

#### VPN Tailscale (Accès administratif)
**Autorisations :**
- Réservé à l'équipe IT Support
- Direction sur demande justifiée (consultation uniquement)
- MFA obligatoire pour tous les utilisateurs
- Révision mensuelle des appareils autorisés

**Sécurité :**
- Protocole WireGuard (moderne et sécurisé)
- Chiffrement intégré
- Logs de connexion activés
- Notification à chaque nouvelle connexion

---

### 3.3 Accès WiFi (Futur - Phase 2)

**Réseau WiFi employés :**
- SSID : YMMO-Corporate
- Sécurité : WPA3-Enterprise (802.1X)
- Authentification : Active Directory
- Isolation client : Activée
- VLAN : 20 (séparé du réseau filaire)

**Réseau WiFi invités :**
- SSID : YMMO-Guest
- Sécurité : WPA2-PSK
- Isolation totale du réseau interne
- Limitation de bande passante
- Portal captif avec acceptation CGU
- VLAN : 30 (isolé)

---

## 4. POLITIQUE DE SÉCURITÉ DES SERVEURS

### 4.1 Durcissement système (Hardening)

#### Windows Server (DC-SIEGE)
✅ **Mesures appliquées :**
- Mises à jour automatiques activées
- Antivirus Windows Defender actif et à jour
- Firewall Windows activé
- Services inutiles désactivés
- Audit de sécurité activé
- BitLocker pour chiffrement du disque (recommandé en production)
- Comptes administrateurs locaux désactivés sauf nécessaire
- Session RDP sécurisée (NLA obligatoire)

#### Linux Servers (SRV-WEB-BDD, SRV-DOCKER)
✅ **Mesures appliquées :**
- Mises à jour automatiques (unattended-upgrades)
- Fail2ban pour protection bruteforce SSH
- SSH : Port 22, clés uniquement (pas de mot de passe), root login désactivé
- UFW (Uncomplicated Firewall) activé
- SELinux ou AppArmor activé
- Services limités au strict nécessaire
- Chiffrement disque LUKS (recommandé en production)

---

### 4.2 Gestion des accès administrateurs

#### Principe
- **Moindre privilège :** Accès admin uniquement quand nécessaire
- **Comptes dédiés :** Un compte utilisateur standard + un compte admin séparé
- **Traçabilité :** Tous les accès admin sont journalisés
- **Révision :** Audit trimestriel des comptes admin

#### Comptes Windows
- **Administrateur local :** Désactivé (sauf urgence)
- **Domain Admins :** YMMO\tadmin (IT Support uniquement)
- **Utilisateurs standards :** Pas de droits admin locaux

#### Comptes Linux (SSH)
- **root :** Connexion SSH désactivée
- **sudo :** Groupe sudo limité aux membres IT Support
- **Clés SSH :** Obligatoires, mots de passe SSH désactivés
- **Bastion host :** Recommandé en production (accès via jump server)

---

### 4.3 Patch Management

#### Politique de mise à jour
- **Mises à jour critiques (sécurité) :** Sous 7 jours
- **Mises à jour importantes :** Sous 30 jours
- **Mises à jour optionnelles :** Évaluation au cas par cas

#### Processus
1. **Veille :** Monitoring des bulletins de sécurité (Microsoft, Ubuntu, etc.)
2. **Test :** Validation en environnement de test (si possible)
3. **Planification :** Fenêtre de maintenance définie
4. **Application :** Déploiement des patches
5. **Vérification :** Tests post-installation
6. **Documentation :** Enregistrement des changements

#### Fenêtres de maintenance
- **Serveurs critiques (AD, DNS, DHCP) :** Samedi 22h-02h
- **Serveurs applicatifs :** Dimanche 22h-02h
- **Postes de travail :** Mercredi 19h-21h (hors heures bureau)
- **Urgence (faille critique 0-day) :** Immédiat avec validation Direction

---

## 5. POLITIQUE DE SAUVEGARDE

### 5.1 Règle 3-2-1

**3 copies des données :**
- 1 copie en production (serveurs)
- 1 copie sur NAS local
- 1 copie hors site (cloud Azure)

**2 supports différents :**
- Disques locaux (serveurs)
- NAS avec RAID 5

**1 copie hors site :**
- Réplication cloud Azure

---

### 5.2 Fréquence et rétention

| Système | Fréquence | Rétention | Destination |
|---------|-----------|-----------|-------------|
| **Active Directory System State** | Quotidienne 02h00 | 14 jours | NAS + Azure |
| **Base de données MySQL** | Quotidienne 01h00 | 30 jours | NAS + Azure |
| **Partages réseau** | Quotidienne 03h00 | 90 jours | NAS + Azure |
| **Configurations système** | Hebdomadaire Dimanche | 12 semaines | NAS |
| **Snapshots VMs** | Hebdomadaire Samedi | 4 semaines | Local |

---

### 5.3 Tests de restauration

**Fréquence :** Mensuelle

**Processus :**
1. Sélection d'une sauvegarde au hasard
2. Restauration en environnement de test isolé
3. Vérification de l'intégrité des données
4. Documentation du test (succès/échec)
5. Correction des problèmes identifiés

**Objectifs :**
- RTO (Recovery Time Objective) : 4 heures
- RPO (Recovery Point Objective) : 24 heures

---

## 6. POLITIQUE DE PROTECTION DES DONNÉES

### 6.1 Classification des données

#### Niveau 1 - Public
- **Exemples :** Brochures commerciales, site web public
- **Protection :** Aucune restriction particulière
- **Stockage :** Serveur web, partages publics

#### Niveau 2 - Interne
- **Exemples :** Documents de travail, emails internes
- **Protection :** Accès authentifié requis
- **Stockage :** Partages réseau départementaux

#### Niveau 3 - Confidentiel
- **Exemples :** Données clients, transactions immobilières
- **Protection :** Accès restreint selon les rôles
- **Stockage :** Base de données chiffrée, partages restreints

#### Niveau 4 - Secret
- **Exemples :** Données RH (salaires), contrats stratégiques, mots de passe
- **Protection :** Chiffrement obligatoire, accès minimal
- **Stockage :** Coffre-fort de mots de passe, partages RH isolés

---

### 6.2 Chiffrement

#### En transit
- **HTTPS :** Obligatoire pour toutes les applications web (TLS 1.2 minimum)
- **VPN :** IPSec avec AES-256 pour tout trafic inter-sites
- **Email :** TLS obligatoire pour SMTP (si email hébergé)
- **SMB :** SMB3 avec chiffrement activé

#### Au repos
- **Disques serveurs :** BitLocker (Windows) ou LUKS (Linux) en production
- **Base de données :** Chiffrement transparent des données (TDE) pour données sensibles
- **NAS :** Chiffrement natif Synology activé
- **Sauvegardes :** Chiffrées avant envoi vers le cloud

---

### 6.3 Conformité RGPD

#### Principes
- **Licéité :** Traitement uniquement avec base légale
- **Limitation de finalité :** Données collectées pour usage défini
- **Minimisation :** Collecter uniquement le nécessaire
- **Exactitude :** Maintenir les données à jour
- **Limitation de conservation :** Suppression après expiration du besoin
- **Intégrité et confidentialité :** Protection appropriée

#### Données personnelles traitées
- **Employés :** Identité, coordonnées, données RH
- **Clients :** Identité, coordonnées, historique transactions
- **Prospects :** Coordonnées, préférences immobilières

#### Durée de conservation
- **Données employés actifs :** Durée du contrat
- **Données employés partis :** 5 ans (obligations légales)
- **Données clients :** 3 ans après dernière transaction
- **Données prospects sans conversion :** 3 ans après dernier contact
- **Logs techniques :** 3-12 mois selon le type

#### Droits des personnes
- **Droit d'accès :** Demande à rh@ymmo.local
- **Droit de rectification :** Demande à rh@ymmo.local
- **Droit à l'effacement :** Après délais légaux
- **Droit à la portabilité :** Export des données sur demande
- **Droit d'opposition :** Possibilité de refuser certains traitements

**DPO (Délégué à la Protection des Données) :** dpo@ymmo.local

---

## 7. POLITIQUE DE DÉTECTION ET RÉPONSE AUX INCIDENTS

### 7.1 Détection

#### Monitoring actif
- **Uptime Kuma :** Surveillance disponibilité services (intervalle 60-120s)
- **Zabbix :** Surveillance performance et métriques systèmes
- **Logs centralisés :** Agrégation des logs dans Zabbix
- **Alertes :** Email + notification en temps réel pour incidents critiques

#### Indicateurs surveillés
- Disponibilité des services (ping, HTTP checks)
- Usage CPU > 80% pendant 5 minutes
- Usage RAM > 85%
- Espace disque < 20%
- Connexions VPN down
- Tentatives de connexion échouées (bruteforce)
- Modifications non autorisées de fichiers système

---

### 7.2 Classification des incidents

| Niveau | Critère | Temps de réponse |
|--------|---------|------------------|
| **Critique** | Service vital indisponible (AD, DNS, VPN) | Immédiat (< 15 min) |
| **Majeur** | Service important dégradé (Web, BDD) | < 1 heure |
| **Mineur** | Service non critique affecté | < 4 heures |
| **Bas** | Problème cosmétique ou documentation | < 24 heures |

---

### 7.3 Procédure de réponse aux incidents

#### Phase 1 - Détection et déclaration
1. Incident détecté (monitoring ou utilisateur)
2. Création ticket dans système de ticketing
3. Classification de la gravité
4. Notification de l'équipe IT Support

#### Phase 2 - Confinement
1. Isolation du système compromis si nécessaire
2. Préservation des preuves (logs, snapshots)
3. Communication aux parties prenantes

#### Phase 3 - Éradication
1. Identification de la cause racine
2. Suppression de la menace
3. Correction de la vulnérabilité

#### Phase 4 - Récupération
1. Restauration du service
2. Vérification du fonctionnement normal
3. Surveillance renforcée temporaire

#### Phase 5 - Post-mortem
1. Rédaction du rapport d'incident
2. Identification des améliorations
3. Mise à jour de la documentation
4. Formation si nécessaire

---

### 7.4 Contacts d'urgence

| Incident | Contact | Disponibilité |
|----------|---------|---------------|
| **Sécurité critique** | security@ymmo.local | 24/7 |
| **Panne système** | it-support@ymmo.local | Horaires bureau + astreinte |
| **Fuite de données** | dpo@ymmo.local + direction@ymmo.local | Immédiat |
| **Cyberattaque** | security@ymmo.local + ANSSI si nécessaire | Immédiat |

---

## 8. POLITIQUE D'UTILISATION ACCEPTABLE

### 8.1 Utilisation du matériel informatique

✅ **Autorisé :**
- Utilisation professionnelle des équipements
- Usage personnel raisonnable (consultation email personnel, actualités)
- Installation de logiciels avec validation IT Support

❌ **Interdit :**
- Téléchargement de contenus illégaux
- Streaming vidéo prolongé (sauf professionnel)
- Installation de logiciels piratés
- Contournement des mesures de sécurité
- Utilisation à des fins personnelles lucratives

---

### 8.2 Utilisation d'Internet et de la messagerie

✅ **Autorisé :**
- Navigation web professionnelle
- Consultation d'actualités pendant les pauses
- Emails personnels occasionnels

❌ **Interdit :**
- Sites à contenu illicite, violent, pornographique
- Téléchargement de fichiers piratés
- Envoi de spam ou chaînes d'emails
- Partage d'informations confidentielles par email non chiffré
- Ouverture de pièces jointes suspectes

---

### 8.3 Utilisation des appareils personnels (BYOD)

**Politique actuelle :** Non autorisé (LAB/Production Phase 1)

**Si implémenté (Phase 2) :**
- Enregistrement obligatoire auprès IT Support
- Installation d'un MDM (Mobile Device Management)
- Respect de la politique de sécurité YMMO
- Séparation données professionnelles/personnelles
- Possibilité d'effacement à distance en cas de perte

---

## 9. SENSIBILISATION ET FORMATION

### 9.1 Formation initiale

**Tous les nouveaux employés :**
- Session de sensibilisation à la sécurité (2 heures)
- Remise du guide de bonnes pratiques
- Signature de la charte d'utilisation
- Formation aux outils (AD, application web, partages)

---

### 9.2 Formation continue

**Fréquence :** Annuelle

**Contenu :**
- Rappel des bonnes pratiques
- Présentation des nouvelles menaces (phishing, ransomware)
- Exercices pratiques (identifier un email malveillant)
- Mise à jour des procédures

---

### 9.3 Tests de phishing

**Fréquence :** Trimestrielle

**Processus :**
1. IT Support envoie un email de phishing simulé
2. Tracking des utilisateurs ayant cliqué
3. Formation personnalisée pour les utilisateurs ayant échoué
4. Rapport anonymisé à la direction

**Pas de sanction disciplinaire pour les tests, seulement formation.**

---

## 10. CONFORMITÉ ET AUDIT

### 10.1 Audit de sécurité

**Fréquence :** Semestrielle

**Éléments audités :**
- Comptes utilisateurs actifs
- Permissions et groupes AD
- Règles firewall
- Logs de sécurité
- Sauvegardes (intégrité et tests)
- Conformité aux politiques

---

### 10.2 Indicateurs de sécurité (KPI)

| Indicateur | Objectif | Mesure |
|------------|----------|--------|
| Disponibilité services critiques | > 99.5% | Uptime Kuma |
| Temps de résolution incident critique | < 4h | Ticketing |
| Sauvegardes réussies | 100% | Logs Zabbix |
| Comptes inactifs désactivés | < 7 jours | Audit AD |
| Patches de sécurité appliqués | < 7 jours | Inventaire |
| Formation sécurité employés | 100%/an | RH |

---

## 11. SANCTIONS

### 11.1 Non-respect de la politique

**Violations mineures :**
- Premier avertissement : Rappel écrit
- Second avertissement : Entretien avec manager + IT
- Troisième avertissement : Sanction RH

**Violations graves :**
- Compromission intentionnelle de la sécurité
- Vol ou fuite de données
- Installation de malware volontaire
- Accès non autorisé aux systèmes

**Conséquences :** Sanctions pouvant aller jusqu'au licenciement + poursuites légales si applicable.

---

## 12. RÉVISIONS DE LA POLITIQUE

**Fréquence de révision :** Annuelle (ou après incident majeur)

**Processus :**
1. Revue par IT Support
2. Consultation des managers
3. Validation par la Direction
4. Communication à tous les employés
5. Formation sur les changements si nécessaire

---

## 13. ACCEPTATION

Tous les employés de YMMO doivent lire, comprendre et accepter cette politique de sécurité.

**Déclaration d'acceptation :**

Je, soussigné(e) _________________________________, reconnais avoir lu et compris la Politique de Sécurité de YMMO. Je m'engage à respecter l'ensemble des règles et procédures définies dans ce document.

**Nom :** _______________________  
**Prénom :** _______________________  
**Service :** _______________________  
**Date :** _______________________  
**Signature :** _______________________

---

## ANNEXES

### Annexe A - Glossaire
- **AD :** Active Directory
- **ANSSI :** Agence Nationale de la Sécurité des Systèmes d'Information
- **DHCP :** Dynamic Host Configuration Protocol
- **DNS :** Domain Name System
- **DPO :** Data Protection Officer (Délégué à la Protection des Données)
- **GPO :** Group Policy Object
- **IDS/IPS :** Intrusion Detection/Prevention System
- **IPSec :** Internet Protocol Security
- **MFA :** Multi-Factor Authentication
- **NAT :** Network Address Translation
- **PSK :** Pre-Shared Key
- **RGPD :** Règlement Général sur la Protection des Données
- **RTO :** Recovery Time Objective
- **RPO :** Recovery Point Objective
- **VPN :** Virtual Private Network

### Annexe B - Contacts utiles
- **IT Support :** it-support@ymmo.local / +33 X XX XX XX XX
- **Sécurité :** security@ymmo.local
- **DPO :** dpo@ymmo.local
- **RH :** rh@ymmo.local
- **ANSSI :** 01 71 75 84 68 (numéro d'urgence cybersécurité)

---

**Approuvé par :**
- **Direction Générale YMMO**
- **Responsable IT Support**
- **DPO YMMO**

**Date d'application :** Février 2026  
**Prochaine révision :** Février 2027  
**Version :** 1.0

import bcrypt

class Utilisateur:
    """Représente un utilisateur (Entité)"""
    def __init__(self, id, nom, prenom, email, mdp, telephone, role):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mdp = mdp
        self.telephone = telephone
        self.role = role

class UtilisateurRepository:
    """Gère la communication avec la table 'utilisateur'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all(self):
        cur = self.db.cursor()
        # On sélectionne exactement les colonnes dans l'ordre du __init__
        cur.execute("SELECT id_utilisateur, nom, prenom, email, mdp, telephone, role FROM utilisateur")
        rows = cur.fetchall()

        # On crée une liste d'objets 'Utilisateur' (en français)
        utilisateurs = [Utilisateur(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]

        cur.close()
        return utilisateurs

    def verifieMdp(self, mdp_propose, mdp_hache_db):
        # On compare le mot de passe tapé avec celui de la base
        return bcrypt.checkpw(mdp_propose.encode('utf-8'), mdp_hache_db.encode('utf-8'))

    def createUtilisateur(self, nom, prenom, email, mdp_clair, telephone, role):
        # 1. On transforme le texte en "sel" (salt) et on hache
        sel = bcrypt.gensalt()
        mdp_hache = bcrypt.hashpw(mdp_clair.encode('utf-8'), sel)

        # 2. On enregistre en base (le mdp_hache est une chaîne d'octets)
        cur = self.db.cursor()
        cur.execute("INSERT INTO utilisateur (nom, prenom, email, mdp, telephone, role) VALUES (%s, %s, %s, %s, %s, %s)", (nom, prenom, email, mdp_hache.decode('utf-8'), telephone, role))
        self.db.commit()
        cur.close()


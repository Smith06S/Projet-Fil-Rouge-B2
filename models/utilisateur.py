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
    def get_by_email(self, email):
        cur = self.db.cursor()
        cur.execute("SELECT id_utilisateur, nom, prenom, email, mdp, telephone, role FROM utilisateur WHERE email = %s", (email,))
        row = cur.fetchone()
        cur.close()
        if row:
            return Utilisateur(*row)
        return None

    def get_by_id(self, user_id):
        cur = self.db.cursor()
        cur.execute("SELECT id_utilisateur, nom, prenom, email, mdp, telephone, role FROM utilisateur WHERE id_utilisateur = %s", (user_id,))
        row = cur.fetchone()
        cur.close()
        if row:
            return Utilisateur(*row)
        return None

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
    
    def hashPassword(self, mdp_clair):
        sel = bcrypt.gensalt()
        mdp_hache = bcrypt.hashpw(mdp_clair.encode('utf-8'), sel)
        return mdp_hache.decode('utf-8')

    def verifieMdp(self, mdp_propose, email):
        cur = self.db.cursor()
        cur.execute("SELECT mdp FROM utilisateur WHERE email = %s", (email,))
        row = cur.fetchone()
        cur.close()
        if row is None:
            return False
        mdp_hache_db = row[0]
        return bcrypt.checkpw(mdp_propose.encode('utf-8'), mdp_hache_db.encode('utf-8'))

    def createUtilisateur(self, nom, prenom, email, mdp_clair, telephone, role):
        mdp_hache = self.hashPassword(mdp_clair)
        cur = self.db.cursor()
        cur.execute("INSERT INTO utilisateur (nom, prenom, email, mdp, telephone, role) VALUES (%s, %s, %s, %s, %s, %s)", (nom, prenom, email, mdp_hache, telephone, role))
        cur.close()

    def find_profil(self, id):
        cur = self.db.cursor()
        cur.execute("SELECT nom, prenom, email, mdp, telephone, role FROM utilisateur WHERE id_utilisateur = %s", (id,))
        row = cur.fetchone()
        cur.close()
        if row:
            return Utilisateur(*row)
        else:
            return None
        

    def is_Admin(self, id_user):
        cur = self.db.cursor()
        cur.execute("SELECT 1 FROM utilisateur WHERE id_utilisateur = %s AND role = 'admin'", (id_user,))
        result = cur.fetchone()
        cur.close()
        return result is not None


    def delete_User(self, id_user):
        cur = self.db.cursor() 
        cur.execute("DELETE FROM utilisateur WHERE id_utilisateur = %s", (id_user,))
        self.db.commit()
        cur.close()


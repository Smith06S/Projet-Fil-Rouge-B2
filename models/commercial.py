from models.utilisateur import Utilisateur

class Commercial(Utilisateur):
    """Représente un commercial (Entité)"""
    def __init__(self, id_utilisateur, nom, prenom, email, mdp, telephone, role, date_embauche, matricule, id_agence, id_commercial=None):
        super().__init__(id_utilisateur, nom, prenom, email, mdp, telephone, role)
        self.date_embauche = date_embauche
        self.matricule = matricule
        self.id_agence = id_agence
        self.id_commercial = id_commercial

class CommercialRepository:
    """Gère la communication avec la table 'commercial'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all(self):
        cur = self.db.cursor()
        cur.execute("SELECT id_commercial, date_embauche, matricule, id_agence, id_utilisateur, nom, prenom, email, mdp, telephone, role FROM commercial JOIN utilisateur ON commercial.id_utilisateur = utilisateur.id_utilisateur")
        rows = cur.fetchall()

        commercials = [Commercial(r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[1], r[2], r[3], r[0]) for r in rows]

        cur.close()
        return commercials
    
    def get_idAgence(self, id_utilisateur):
        cur = self.db.cursor()
        cur.execute("SELECT id_agence FROM commercial WHERE id_utilisateur = %s", (id_utilisateur,))
        row = cur.fetchone()
        cur.close()
        if row:
            return row[0]
        return None
    
    def is_Commercial(self, id_user):
        cur = self.db.cursor()
        cur.execute("SELECT 1 FROM commercial WHERE id_utilisateur = %s AND role = commercial", (id_user,))
        result = cur.fetchone()
        cur.close()
        return result is not None
    
    def get_Commercial(self, id):
        cur = self.db.cursor()
        cur.execute("SELECT id_commercial, date_embauche, matricule, id_agence, id_utilisateur, nom, prenom, email, mdp, telephone, role FROM commercial JOIN utilisateur ON commercial.id_utilisateur = utilisateur.id_utilisateur WHERE id_user = %s", (id,))
        row = cur.fetchone()
        cur.close()
        if row:
            return Utilisateur(*row)
        else:
            return None

    def delete_Commercial(self, id_user):
        cur = self.db.cursor() 
        cur.execute("DELETE FROM commercial WHERE id_utilisateur = %s", (id_user,))
        self.db.commit()
        cur.close()
    
    def modify_Commercial(self, nom, prenom, email, mdp, telephone, date_embauche, matricule, id_user):
        cur = self.db.cursor()
        cur.execute("""
            UPDATE utilisateur 
            SET nom = %s, prenom = %s, email = %s, mdp = %s, telephone = %s 
            WHERE id_utilisateur = %s;
        """, (nom, prenom, email, mdp, telephone, id_user))
        
        cur.execute("""
            UPDATE commercial 
            SET date_embauche = %s, matricule = %s 
            WHERE id_utilisateur = %s;
        """, (date_embauche, matricule, id_user))
        
        self.db.commit()
        cur.close()

    
    
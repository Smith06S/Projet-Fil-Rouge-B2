from models.utilisateur import Utilisateur

class Client(Utilisateur):
    """Représente un client (Entité)"""
    def __init__(self, id_utilisateur, nom, prenom, email, mdp, telephone, role, type_client, budget_max, id_agence, id_client=None):
        super().__init__(id_utilisateur, nom, prenom, email, mdp, telephone, role)
        self.type_client = type_client
        self.budget_max = budget_max
        self.id_agence = id_agence
        self.id_client = id_client

class ClientRepository:
    """Gère la communication avec la table 'client'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all(self):
        cur = self.db.cursor()
        cur.execute("SELECT id_client, type_client, budget_max, id_agence, id_utilisateur, nom, prenom, email, mdp, telephone, role FROM client JOIN utilisateur ON client.id_utilisateur = utilisateur.id_utilisateur")
        rows = cur.fetchall()

        clients = [Client(r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[1], r[2], r[3], r[0]) for r in rows]

        cur.close()
        return clients
    
    def is_Client(self, id_user):
        cur = self.db.cursor()
        cur.execute("SELECT 1 FROM client WHERE id_utilisateur = %s", (id_user,))
        result = cur.fetchone()
        cur.close()
        return result is not None
    
    def get_Client(self, id):
        cur = self.db.cursor()
        cur.execute("SELECT id_client, type_client, budget_max, id_agence, id_utilisateur, nom, prenom, email, mdp, telephone, role FROM client JOIN utilisateur ON client.id_utilisateur = utilisateur.id_utilisateur WHERE id_user = %s", (id,))
        row = cur.fetchone()
        cur.close()
        if row:
            return Utilisateur(*row)
        else:
            return None
class Agence:
    """Représente une agence (Entité)"""
    def __init__(self, id, nom, ville, code_postal):
        self.id = id
        self.nom = nom
        self.ville = ville
        self.code_postal = code_postal

class AgenceRepository:
    """Gère la communication avec la table 'agence'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all(self):
        cur = self.db.cursor()
        cur.execute("SELECT id_agence, nom_agence, ville, code_postal FROM agence")
        rows = cur.fetchall()

        agences = [Agence(r[0], r[1], r[2], r[3]) for r in rows]

        cur.close()
        return agences

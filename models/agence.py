class Agence:
    def __init__(self, id_agence, nom, ville, adresse):
        self.id_agence = id_agence
        self.nom = nom
        self.ville = ville
        self.adresse = adresse

class AgenceRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def find_all(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT id_agence, nom, ville, adresse FROM agence")
            return [Agence(**row) for row in cur.fetchall()]

    def get_by_id(self, id_agence):
        with self.db.cursor() as cur:
            cur.execute("SELECT id_agence, nom, ville, adresse FROM agence WHERE id_agence = %s", (id_agence,))
            row = cur.fetchone()
            return Agence(**row) if row else None
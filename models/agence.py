class Agence:
    def __init__(self, id_agence, nom, ville, adresse, image_url=None):
        self.id_agence = id_agence
        self.nom = nom
        self.ville = ville
        self.adresse = adresse
        self.image_url = image_url or 'static/images/default_agence.jpg'

class AgenceRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def find_all(self):
        with self.db.cursor() as cur:
            cur.execute("SELECT id_agence, nom, ville, adresse, image_url FROM agence")
            return [Agence(**row) for row in cur.fetchall()]

    def get_by_id(self, id_agence):
        with self.db.cursor() as cur:
            cur.execute("SELECT id_agence, nom, ville, adresse, image_url FROM agence WHERE id_agence = %s", (id_agence,))
            row = cur.fetchone()
            return Agence(**row) if row else None

    def get_top_5_agences_favoris(self):
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT a.id_agence, a.nom, a.ville, a.adresse, a.image_url, COUNT(f.id_favoris) as nb_favoris
                FROM agence a
                LEFT JOIN bien b ON a.id_agence = b.id_agence
                LEFT JOIN favoris f ON b.id_bien = f.id_bien
                GROUP BY a.id_agence, a.nom, a.ville, a.adresse, a.image_url
                ORDER BY nb_favoris DESC
                LIMIT 5
            """)
            return [Agence(**row) for row in cur.fetchall()]
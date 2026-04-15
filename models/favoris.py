class Favoris:
    """Représente un favoris (Entité)"""
    def __init__(self, id_favoris, id_bien, id_client):
        self.id_favoris = id_favoris
        self.id_bien = id_bien
        self.id_client = id_client

class FavorisRepository:
    """Gère la communication avec la table 'favoris'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all(self):
        cur = self.db.cursor()
        cur.execute("SELECT id_favoris, id_bien, id_client FROM favoris")
        rows = cur.fetchall()

        favoris = [Favoris(r[0], r[1], r[2]) for r in rows]

        cur.close()
        return favoris
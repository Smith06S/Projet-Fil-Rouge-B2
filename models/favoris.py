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

    def find_all_by_user(self, id_client):
        cur = self.db.cursor()
        cur.execute("SELECT id_favoris, id_bien, id_client FROM favoris WHERE id_client = %s", (id_client,))
        rows = cur.fetchall()

        favoris = [Favoris(r[0], r[1], r[2]) for r in rows]

        cur.close()
        return favoris

    def add_to_favoris(self, id_bien, id_client):
        cur = self.db.cursor()
        cur.execute("INSERT INTO favoris (id_bien, id_client) VALUES (%s, %s)", (id_bien, id_client))
        self.db.commit()
        cur.close()

    def remove_from_favoris(self, id_bien, id_client):
        cur = self.db.cursor()
        cur.execute("DELETE FROM favoris WHERE id_bien = %s AND id_client = %s", (id_bien, id_client))
        self.db.commit()
        cur.close()

    def favoris_exists(self, id_bien, id_client):
        cur = self.db.cursor()
        cur.execute("SELECT 1 FROM favoris WHERE id_bien = %s AND id_client = %s", (id_bien, id_client))
        result = cur.fetchone()
        cur.close()
        return result is not None
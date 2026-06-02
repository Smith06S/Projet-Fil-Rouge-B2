class Panier:
    """Représente un article dans le panier (Entité)"""
    def __init__(self, id_panier, id_bien, id_client, date_ajout=None):
        self.id_panier = id_panier
        self.id_bien = id_bien
        self.id_client = id_client
        self.date_ajout = date_ajout

class PanierRepository:
    """Gère la communication avec la table 'panier'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all_by_user(self, id_client):
        cur = self.db.cursor()
        cur.execute("SELECT id_panier, id_bien, id_client, date_ajout FROM panier WHERE id_client = %s ORDER BY date_ajout DESC", (id_client,))
        rows = cur.fetchall()
        panier = [Panier(r[0], r[1], r[2], r[3]) for r in rows]
        cur.close()
        return panier

    def add_to_panier(self, id_bien, id_client):
        cur = self.db.cursor()
        cur.execute("INSERT INTO panier (id_bien, id_client, date_ajout) VALUES (%s, %s, NOW())", (id_bien, id_client))
        self.db.commit()
        cur.close()

    def remove_from_panier(self, id_panier):
        cur = self.db.cursor()
        cur.execute("DELETE FROM panier WHERE id_panier = %s", (id_panier,))
        self.db.commit()
        cur.close()

    def remove_bien_from_panier(self, id_bien, id_client):
        cur = self.db.cursor()
        cur.execute("DELETE FROM panier WHERE id_bien = %s AND id_client = %s", (id_bien, id_client))
        self.db.commit()
        cur.close()

    def panier_exists(self, id_bien, id_client):
        cur = self.db.cursor()
        cur.execute("SELECT 1 FROM panier WHERE id_bien = %s AND id_client = %s", (id_bien, id_client))
        result = cur.fetchone()
        cur.close()
        return result is not None

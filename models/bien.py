class Bien:
    def __init__(self, id_bien, ville, adresse, description, nbr_pieces, surface, type_bien, prix, statut, id_commercial, id_agence):
        self.id_bien = id_bien
        self.ville = ville
        self.adresse = adresse
        self.description = description
        self.nbr_pieces = nbr_pieces
        self.surface = surface
        self.type_bien = type_bien
        self.prix = prix
        self.statut = statut
        self.id_commercial = id_commercial
        self.id_agence = id_agence

class BienRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def find_all_by_agence(self, id_agence):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM bien WHERE id_agence = %s AND statut = 'Disponible'", (id_agence,))
            return [Bien(**row) for row in cur.fetchall()]

    def get_by_id(self, id_bien):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM bien WHERE id_bien = %s", (id_bien,))
            row = cur.fetchone()
            return Bien(**row) if row else None

    def create(self, ville, adresse, description, nbr_pieces, surface, type_bien, prix, id_commercial, id_agence):
        with self.db.cursor() as cur:
            cur.execute("""INSERT INTO bien (ville, adresse, description, nbr_pieces, surface, type_bien, prix, statut, id_commercial, id_agence) VALUES (%s, %s, %s, %s, %s, %s, %s, 'Disponible', %s, %s)""", (ville, adresse, description, nbr_pieces, surface, type_bien, prix, id_commercial, id_agence))
        self.db.commit()

    def update(self, id_bien, ville, adresse, description, nbr_pieces, surface, type_bien, prix, statut):
        with self.db.cursor() as cur:
            cur.execute("""UPDATE bien SET ville=%s, adresse=%s, description=%s, nbr_pieces=%s, surface=%s, type_bien=%s, prix=%s, statut=%s WHERE id_bien=%s """, (ville, adresse, description, nbr_pieces, surface, type_bien, prix, statut, id_bien))
        self.db.commit()

    def delete(self, id_bien):
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM bien WHERE id_bien = %s", (id_bien,))
        self.db.commit()

    def find_by_filter(self, ville=None, prix_max=None, type_bien=None):
        with self.db.cursor() as cur:
            query = "SELECT * FROM bien WHERE statut = 'Disponible'"
            params = []
            if ville:
                query += " AND ville ILIKE %s"
                params.append(f"%{ville}%")
            if prix_max:
                query += " AND prix <= %s"
                params.append(prix_max)
            if type_bien:
                query += " AND type_bien = %s"
                params.append(type_bien)
            cur.execute(query, params)
            return [Bien(**row) for row in cur.fetchall()]
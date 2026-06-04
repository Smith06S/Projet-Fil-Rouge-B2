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
            if row:
                bien_data = dict(row)                
                cur.execute("SELECT image_url FROM photo_bien WHERE id_bien = %s", (id_bien,))
                photos_rows = cur.fetchall()
                bien_data['photos'] = [p['image_url'] for p in photos_rows]
                return bien_data
            return None

    def create(self, ville, adresse, description, nbr_pieces, surface, type_bien, prix, id_commercial, id_agence):
        with self.db.cursor() as cur:
            # On ajoute RETURNING id_bien à la fin de la requête
            cur.execute("""
                INSERT INTO bien (ville, adresse, description, nbr_pieces, surface, type_bien, prix, statut, id_commercial, id_agence) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Disponible', %s, %s)
                RETURNING id_bien
            """, (ville, adresse, description, nbr_pieces, surface, type_bien, prix, id_commercial, id_agence))
            id_bien = cur.fetchone()['id_bien']
        self.db.commit()
        return id_bien  # On retourne l'id pour le contrôleur

    def add_photo(self, id_bien, image_url):
        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO photo_bien (image_url, id_bien)
                VALUES (%s, %s)
            """, (image_url, id_bien))
        self.db.commit()

    def delete(self, id_bien):
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM bien WHERE id_bien = %s", (id_bien,))
        self.db.commit()

    def find_by_filter(self, id_agence, ville=None, prix_max=None, type_bien=None):
        with self.db.cursor() as cur:
            query = "SELECT * FROM bien WHERE id_agence = %s AND statut = 'Disponible'"
            params = [id_agence]            
            if ville and ville.strip() != "":
                query += " AND ville ILIKE %s"
                params.append(f"%{ville}%")
            if prix_max and str(prix_max).strip() != "":
                query += " AND prix <= %s"
                params.append(float(prix_max))
            if type_bien and type_bien.strip() != "":
                query += " AND type_bien = %s"
                params.append(type_bien)
                
            cur.execute(query, params)
            return [Bien(**row) for row in cur.fetchall()]

    def add_favoris(self, id_client, id_bien):
        with self.db.cursor() as cur:
            cur.execute("INSERT INTO favoris (id_client, id_bien) VALUES (%s, %s) ON CONFLICT DO NOTHING", (id_client, id_bien))
        self.db.commit()

    def remove_favoris(self, id_client, id_bien):
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM favoris WHERE id_client = %s AND id_bien = %s", (id_client, id_bien))
        self.db.commit()

    def get_favoris_by_client(self, id_client):
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT b.* FROM bien b
                JOIN favoris f ON b.id_bien = f.id_bien
                WHERE f.id_client = %s
            """, (id_client,))
            return [Bien(**row) for row in cur.fetchall()]
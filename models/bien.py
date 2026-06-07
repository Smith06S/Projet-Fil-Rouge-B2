class Bien:
    def __init__(self, id_bien, ville, adresse, description, nbr_pieces, surface, type_bien, prix, statut, id_commercial, id_agence, nbr_chambres=0, a_balcon=False, a_parking=False, type_chauffage='Non renseigné', etage='Rez-de-chaussée', a_ascenseur=False, etat_logement='Bon état', annee_construction=None):
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
        self.nbr_chambres = nbr_chambres
        self.a_balcon = a_balcon
        self.a_parking = a_parking
        self.type_chauffage = type_chauffage
        self.etage = etage
        self.a_ascenseur = a_ascenseur
        self.etat_logement = etat_logement
        self.annee_construction = annee_construction

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

    def create(self, ville, adresse, description, nbr_pieces, surface, type_bien, prix, id_commercial, id_agence, nbr_chambres, a_balcon, a_parking, type_chauffage, etage, a_ascenseur, etat_logement, annee_construction):
        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO bien (ville, adresse, description, nbr_pieces, surface, type_bien, prix, statut, id_commercial, id_agence, nbr_chambres, a_balcon, a_parking, type_chauffage, etage, a_ascenseur, etat_logement, annee_construction) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Disponible', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_bien
            """, (ville, adresse, description, nbr_pieces, surface, type_bien, prix, id_commercial, id_agence, nbr_chambres, a_balcon, a_parking, type_chauffage, etage, a_ascenseur, etat_logement, annee_construction))
            id_bien = cur.fetchone()['id_bien']
        self.db.commit()
        return id_bien

    def add_photo(self, id_bien, image_url):
        with self.db.cursor() as cur:
            cur.execute("INSERT INTO photo_bien (image_url, id_bien) VALUES (%s, %s)", (image_url, id_bien))
        self.db.commit()

    def delete(self, id_bien):
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM bien WHERE id_bien = %s", (id_bien,))
        self.db.commit()

    def find_by_filter(self, id_agence, ville=None, prix_max=None, type_bien=None, nbr_chambres_min=None, avec_balcon=False, avec_parking=False, type_chauffage=None, avec_ascenseur=False, etat_logement=None):
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
            if nbr_chambres_min and str(nbr_chambres_min).strip() != "":
                query += " AND nbr_chambres >= %s"
                params.append(int(nbr_chambres_min))
            if type_chauffage and type_chauffage.strip() != "":
                query += " AND type_chauffage = %s"
                params.append(type_chauffage)
            if etat_logement and etat_logement.strip() != "":
                query += " AND etat_logement = %s"
                params.append(etat_logement)
            if avec_balcon:
                query += " AND a_balcon = TRUE"
            if avec_parking:
                query += " AND a_parking = TRUE"
            if avec_ascenseur:
                query += " AND a_ascenseur = TRUE"
                
            cur.execute(query, params)
            biens = []
            for row in cur.fetchall():
                bien = Bien(**row)
                cur.execute("SELECT image_url FROM photo_bien WHERE id_bien = %s", (bien.id_bien,))
                bien.images = [p['image_url'] for p in cur.fetchall()]
                biens.append(bien)
            return biens

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
            cur.execute("SELECT b.* FROM bien b JOIN favoris f ON b.id_bien = f.id_bien WHERE f.id_client = %s", (id_client,))
            return [Bien(**row) for row in cur.fetchall()]
        
    def update(self, id_bien, ville, adresse, description, nbr_pieces, surface, type_bien, prix, nbr_chambres, a_balcon, a_parking, type_chauffage, etage, a_ascenseur, etat_logement, annee_construction):
        with self.db.cursor() as cur:
            cur.execute("""
                UPDATE bien 
                SET ville = %s, adresse = %s, description = %s, nbr_pieces = %s, surface = %s, 
                    type_bien = %s, prix = %s, nbr_chambres = %s, a_balcon = %s, a_parking = %s, 
                    type_chauffage = %s, etage = %s, a_ascenseur = %s, etat_logement = %s, annee_construction = %s
                WHERE id_bien = %s
            """, (ville, adresse, description, nbr_pieces, surface, type_bien, prix, nbr_chambres, a_balcon, a_parking, type_chauffage, etage, a_ascenseur, etat_logement, annee_construction, id_bien))
        self.db.commit()
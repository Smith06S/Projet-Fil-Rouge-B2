class Bien:
    """Représente un bien (Entité)"""
    def __init__(self,  id_bien, ville, adresse, description, nbr_pieces, surface, type_bien, exposition=None, etat_logement=None, energie_chauffage=None, type_eau_chaude=None, type_chauffage=None, moyen_eau_chaude=None, etage=None, vue=None, prix=None, statut=None, id_commercial=None, id_statistique=None, id_agence=None):
        self.id = id_bien
        self.ville = ville
        self.adresse = adresse
        self.description = description
        self.nbr_pieces = nbr_pieces
        self.surface = surface
        self.type_bien = type_bien
        self.exposition = exposition
        self.etat_logement = etat_logement
        self.energie_chauffage = energie_chauffage
        self.type_eau_chaude = type_eau_chaude
        self.type_chauffage = type_chauffage
        self.moyen_eau_chaude = moyen_eau_chaude
        self.etage = etage
        self.vue = vue
        self.prix = prix
        self.statut = statut
        self.id_commercial = id_commercial
        self.id_statistique = id_statistique
        self.id_agence = id_agence

class BienRepository:
    """Gère la communication avec la table 'bien'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all(self):
        cur = self.db.cursor()
        cur.execute("SELECT id_bien, ville, adresse, description, nbr_pieces, surface, type_bien FROM bien")
        rows = cur.fetchall()

        biens = [Bien(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]

        cur.close()
        return biens
    
    def getProduit(self, id):
        cur = self.db.cursor()
        cur.execute("SELECT id_bien, ville, adresse, description, nbr_pieces, surface, type_bien, exposition, etat_logement, energie_chauffage, type_eau_chaude, type_chauffage, moyen_eau_chaude, etage, vue, prix, statut, id_commercial, id_statistique, id_agence FROM bien WHERE id_bien = %s", (id,))
        row = cur.fetchone()
        cur.close()
        if row:
            return Bien(*row)
        else:
            return None

    def find_by_agence(self, id_agence):
        cur = self.db.cursor()
        cur.execute("SELECT id_bien, ville, adresse, description, nbr_pieces, surface, type_bien, exposition, etat_logement, energie_chauffage, type_eau_chaude, type_chauffage, moyen_eau_chaude, etage, vue, prix, statut, id_commercial, id_statistique, id_agence FROM bien WHERE id_agence = %s", (id_agence,))
        rows = cur.fetchall()
        biens = [Bien(*r) for r in rows]
        cur.close()
        return biens
        
    def createBien(self, ville, adresse, description, nbrPieces, surface, typeBien, exposition, etatLogement, energieChauffage, typeEauChaude, typeChauffage, moyenEauChaude, etage, vue, prix, statut, id_commercial, id_agence):
        cur = self.db.cursor()
        cur.execute("INSERT INTO bien (ville, adresse, description, nbr_pieces, surface, type_bien, exposition, etat_logement, energie_chauffage, type_eau_chaude, type_chauffage, moyen_eau_chaude, etage, vue, prix, statut, id_commercial, id_statistique, id_agence) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, %s)", (ville, adresse, description, nbrPieces, surface, typeBien, exposition, etatLogement, energieChauffage, typeEauChaude, typeChauffage, moyenEauChaude, etage, vue, prix, statut, id_commercial, id_agence))
        self.db.commit()
        cur.close()

    def modifyBien(self, id_bien, ville, adresse, description, nbrPieces, surface, typeBien, exposition, etatLogement, energieChauffage, typeEauChaude, typeChauffage, moyenEauChaude, etage, vue, prix, statut, id_agence):
        cur = self.db.cursor()
        cur.execute("UPDATE bien SET ville = %s, adresse = %s, description = %s, nbr_pieces = %s, surface = %s, type_bien = %s, exposition = %s, etat_logement = %s, energie_chauffage = %s, type_eau_chaude = %s, type_chauffage = %s, moyen_eau_chaude = %s, etage = %s, vue = %s, prix = %s, statut = %s, id_statistique = %s, id_agence = %s WHERE id_bien = %s;" , (ville, adresse, description, nbrPieces, surface, typeBien, exposition, etatLogement, energieChauffage, typeEauChaude, typeChauffage, moyenEauChaude, etage, vue, prix, statut, id_agence))
        self.db.commit()
        cur.close()

    def deleteBien(self, id_bien):
        cur = self.db.cursor()
        cur.execute("DELETE FROM bien WHERE id_bien = %s", (id_bien,))
        self.db.commit()
        cur.close()

    def find_by_filter(self, ville=None, prix_max=None, type_bien=None):
        cur = self.db.cursor()
        query = "SELECT id_bien, ville, adresse, description, nbr_pieces, surface, type_bien FROM bien WHERE 1=1"
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
            
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        biens = [Bien(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]
        cur.close()
        return biens
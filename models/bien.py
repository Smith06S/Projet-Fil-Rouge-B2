class Bien:
    """Représente un bien (Entité)"""
    def __init__(self,  id_bien, ville, adresse, description, nbr_pieces, surface, type_bien, exposition, etat_logement, energie_chauffage, type_eau_chaude, type_chauffage, moyen_eau_chaude, etage, vue, prix, statut, id_statistique, id_agence ):
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
        cur.execute("SELECT id_bien, ville, adresse, description, nbr_pieces, surface, type_bien, exposition, etat_logement, energie_chauffage, type_eau_chaude, type_chauffage, moyen_eau_chaude, etage, vue, prix, statut, id_statistique, id_agence FROM bien WHERE id_bien = %s", (id,))
        row = cur.fetchone()
        cur.close()
        if row:
            return Bien(*row)
        else:
            return None
        
    def createBien(self, ville, adresse, description, nbrPieces, surface, typeBien, exposition, etatLogement, energieChauffage, typeEauChaude, typeChauffage, moyenEauChaude, etage, vue, prix, statut, id_agence):
        cur = self.db.cursor()
        # On met id_statistique à NULL par défaut (ou adapte selon ton modèle)
        cur.execute("INSERT INTO bien (ville, adresse, description, nbr_pieces, surface, type_bien, exposition, etat_logement, energie_chauffage, type_eau_chaude, type_chauffage, moyen_eau_chaude, etage, vue, prix, statut, id_statistique, id_agence) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, %s)", (ville, adresse, description, nbrPieces, surface, typeBien, exposition, etatLogement, energieChauffage, typeEauChaude, typeChauffage, moyenEauChaude, etage, vue, prix, statut, id_agence))
        self.db.commit()
        cur.close()



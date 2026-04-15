class Statistique:
    """Représente une statistique (Entité)"""
    def __init__(self, id_statistique, zone_geographique, prix_moyen_m2, indice_popularite, precision_evolution_prix, volume_vente_estime, date_analyse):
        self.id_statistique = id_statistique
        self.zone_geographique = zone_geographique
        self.prix_moyen_m2 = prix_moyen_m2
        self.indice_popularite = indice_popularite
        self.precision_evolution_prix = precision_evolution_prix
        self.volume_vente_estime = volume_vente_estime
        self.date_analyse = date_analyse

class StatistiqueRepository:
    """Gère la communication avec la table 'statistique'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all(self):
        cur = self.db.cursor()
        cur.execute("SELECT id_statistique, zone_geographique, prix_moyen_m2, indice_popularite, precision_evolution_prix, volume_vente_estime, date_analyse FROM statistique")
        rows = cur.fetchall()

        statistiques = [Statistique(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]

        cur.close()
        return statistiques
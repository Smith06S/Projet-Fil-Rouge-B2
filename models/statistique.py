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

    def get_by_zone(self, zone_geographique):
        """Récupère les statistiques d'une ville spécifique"""
        cur = self.db.cursor()
        cur.execute("""
            SELECT id_statistique, zone_geographique, prix_moyen_m2, indice_popularite, precision_evolution_prix, volume_vente_estime, date_analyse 
            FROM statistique WHERE zone_geographique ILIKE %s
        """, (zone_geographique,))
        row = cur.fetchone()
        cur.close()
        if row:
            return Statistique(*row)
        return None

    def calculer_real_stats_from_db(self):
        """
        MODULE DATA AVANCÉ : Traite, nettoie et calcule les tendances 
        marché en fonction des biens réels en base de données.
        """
        cur = self.db.cursor()
        
        # Algorithme d'agrégation : Prix moyen au m² et volume par ville
        cur.execute("""
            SELECT ville, 
                   AVG(prix / NULLIF(surface, 0)) as prix_m2, 
                   COUNT(id_bien) as volume 
            FROM bien 
            GROUP BY ville
        """)
        trends = cur.fetchall()
        
        for t in trends:
            ville = t[0]
            prix_m2 = float(t[1] or 0)
            volume = int(t[2] or 0)
            
            # Calcul de l'indice de popularité (Note sur 10)
            # Plus il y a de biens dans une ville, plus la zone est jugée populaire
            popularity_score = min(volume * 2, 10)
            if popularity_score == 0: 
                popularity_score = 5 # Score neutre par défaut
            
            # Simulation d'évolution prédictive des prix (en %)
            evolution_estimee = round(2.1 + (volume * 0.5), 2)
            
            # Estimation annuelle du volume des ventes locales
            volume_annuel_estime = volume * 8
            
            # Est-ce que cette ville possède déjà une ligne de statistiques ?
            cur.execute("SELECT id_statistique FROM statistique WHERE zone_geographique ILIKE %s", (ville,))
            exists = cur.fetchone()
            
            if exists:
                # Mise à jour (Mise à disposition des rapports mis à jour)
                cur.execute("""
                    UPDATE statistique 
                    SET prix_moyen_m2 = %s, indice_popularite = %s, precision_evolution_prix = %s, volume_vente_estime = %s, date_analyse = NOW()
                    WHERE id_statistique = %s
                """, (prix_m2, popularity_score, evolution_estimee, volume_annuel_estime, exists[0]))
            else:
                # Création d'une nouvelle analyse sectorielle
                cur.execute("""
                    INSERT INTO statistique (zone_geographique, prix_moyen_m2, indice_popularite, precision_evolution_prix, volume_vente_estime, date_analyse)
                    VALUES (%s, %s, %s, %s, %s, NOW())
                """, (ville, prix_m2, popularity_score, evolution_estimee, volume_annuel_estime))
                
        self.db.commit()
        cur.close()
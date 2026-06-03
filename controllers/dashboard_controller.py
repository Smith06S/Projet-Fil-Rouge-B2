from flask import Blueprint, render_template, session
from database import Database
from helpers.auth_helper import role_required

dashboard_bp = Blueprint('dashboard', __name__)
db_manager = Database()

@dashboard_bp.route('/dashboard')
@role_required(['commercial', 'admin'])
def voir_dashboard():
    conn = db_manager.get_connection()
    analyses_predictions = []
    
    with conn.cursor() as cur:
        # 1. Calcul des zones intéressantes où acheter (Prix attractif & Volume actif élevé)
        # 2. Simulation de prédictions de vente (Calcul de la popularité sur les favoris par Ville)
        cur.execute("""
            SELECT 
                b.ville as zone_geographique,
                ROUND(AVG(b.prix / b.surface), 2) as prix_moyen_m2,
                COUNT(f.id_favoris) + 3 as indice_popularite,
                ROUND(5 + (COUNT(f.id_favoris) * 1.5), 1) as precision_evolution_prix,
                COUNT(b.id_bien) * 4 as volume_vente_estime,
                CURRENT_DATE as date_analyse
            FROM bien b
            LEFT JOIN favoris f ON b.id_bien = f.id_bien
            GROUP BY b.ville
            ORDER BY indice_popularite DESC
        """)
        analyses_predictions = cur.fetchall()
        
        # Statistiques générales consolidées
        cur.execute("SELECT COUNT(*) FROM bien WHERE statut = 'Disponible'")
        biens_actifs = cur.fetchone()[0]
        
        cur.execute("SELECT COALESCE(SUM(prix), 0) FROM bien WHERE statut = 'Vendu'")
        ca_total = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM bien WHERE statut = 'Vendu'")
        total_ventes = cur.fetchone()[0]
        
    conn.close()
    
    return render_template(
        'dashboard_stats.html', 
        statistiques=analyses_predictions,
        biens_actifs=biens_actifs,
        ca_total=ca_total,
        total_ventes=total_ventes
    )
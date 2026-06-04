from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from database import Database
from models.utilisateur import UtilisateurRepository
from models.agence import AgenceRepository
from helpers.auth_helper import role_required
import random

dashboard_bp = Blueprint('dashboard', __name__)
db_manager = Database()

@dashboard_bp.route('/dashboard')
@role_required(['commercial', 'admin'])
def voir_dashboard():
    conn = db_manager.get_connection()
    analyses_predictions = []
          
    with conn.cursor() as cur:
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
                  
        cur.execute("SELECT COUNT(*) FROM bien WHERE statut = 'Disponible'")
        biens_actifs = cur.fetchone()[0]
                  
        cur.execute("SELECT COALESCE(SUM(prix), 0) FROM bien WHERE statut = 'Vendu'")
        ca_total = cur.fetchone()[0]
                  
        cur.execute("SELECT COUNT(*) FROM bien WHERE statut = 'Vendu'")
        total_ventes = cur.fetchone()[0]
        
        cur.execute("SELECT id_utilisateur, nom, prenom, email, telephone, role FROM utilisateur")
        utilisateurs_list = cur.fetchall()
              
    conn.close()
          
    return render_template(
        'dashboard_stats.html', 
        statistiques=analyses_predictions,
        biens_actifs=biens_actifs,
        ca_total=ca_total,
        total_ventes=total_ventes,
        utilisateurs=utilisateurs_list
    )

@dashboard_bp.route('/commercial/ajouter', methods=['GET', 'POST'])
@role_required(['commercial', 'admin'])
def ajouter_commercial():
    conn = db_manager.get_connection()
    repo_user = UtilisateurRepository(conn)
    repo_agence = AgenceRepository(conn)
          
    if request.method == 'POST':
        nom = request.form.get('lname')
        prenom = request.form.get('fname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        telephone = request.form.get('phone')
                  
        if password != confirm_password:
            flash("Erreur : Le mot de passe de confirmation diffère du premier saisi.", "error")
            agences = repo_agence.find_all()
            conn.close()
            return render_template('ajouterCommercial.html', agences=agences, id_agence=session.get('id_agence'))

        if session.get('role') == 'admin':
            id_agence = request.form.get('id_agence', type=int)
        else:
            id_agence = session.get('id_agence')
                      
        matricule = f"MAT-{random.randint(1000, 9999)}"
                  
        try:
            repo_user.create_commercial(nom, prenom, email, password, telephone, id_agence, matricule)
            flash(f"Le commercial {prenom} {nom} a été créé avec le matricule {matricule}.", "success")
            return redirect(url_for('auth.voir_profil')) # <-- MODIFICATION : Redirection vers le profil
        except Exception as e:
            conn.rollback()
            flash(f"Erreur de création du compte : {e}", "error")
            return redirect(url_for('auth.voir_profil')) # <-- MODIFICATION : Redirection vers le profil en cas d'échec
                        
    agences = repo_agence.find_all()
    conn.close()
    return render_template('ajouterCommercial.html', agences=agences, id_agence=session.get('id_agence'))
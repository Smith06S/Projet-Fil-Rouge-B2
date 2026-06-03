from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import Database
from models.utilisateur import UtilisateurRepository
from models.agence import AgenceRepository
from models.transaction import TransactionRepository
from helpers.auth_helper import role_required

dashboard_bp = Blueprint('dashboard', __name__)
db_manager = Database()

@dashboard_bp.route('/dashboard')
@role_required(['commercial', 'admin'])
def voir_dashboard():
    conn = db_manager.get_connection()
    stats = {}
    
    with conn.cursor() as cur:
        # 1. Volume total des ventes réelles et chiffre d'affaires cumulé
        cur.execute("SELECT COUNT(*) as total_ventes, COALESCE(SUM(prix_final), 0) as ca_total FROM transaction")
        kpis = cur.fetchone()
        stats['total_ventes'] = kpis['total_ventes']
        stats['ca_total'] = kpis['ca_total']
        
        # 2. Nombre de biens actuellement sur le marché
        cur.execute("SELECT COUNT(*) FROM bien WHERE statut = 'Disponible'")
        stats['biens_actifs'] = cur.fetchone()[0]

        # 3. Data avancée : Analyse et calcul du prix moyen au m² par ville
        cur.execute("""
            SELECT ville, ROUND(AVG(prix / surface), 2) as prix_m2_moyen, COUNT(*) as volume_actifs
            FROM bien WHERE statut = 'Disponible'
            GROUP BY ville ORDER BY prix_m2_moyen DESC
        """)
        stats['analyse_villes'] = cur.fetchall()
        
    conn.close()
    return render_template('dashboard_stats.html', stats=stats)

@dashboard_bp.route('/commercial/ajouter', methods=['GET', 'POST'])
@role_required(['admin']) # Restreint strictement à l'administrateur système
def ajouter_commercial():
    conn = db_manager.get_connection()
    repo_user = UtilisateurRepository(conn)
    repo_agence = AgenceRepository(conn)

    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        id_agence = request.form.get('id_agence', type=int)

        import random
        matricule = f"MAT-{random.randint(1000, 9999)}"

        try:
            repo_user.create_commercial(lname, fname, email, password, phone, id_agence, matricule)
            flash("Compte Commercial créé avec succès.", "success")
            return redirect(url_for('dashboard.voir_dashboard'))
        except Exception as e:
            conn.rollback()
            flash(f"Erreur de création : {e}", "error")

    agences = repo_agence.find_all()
    conn.close()
    return render_template('ajouterCommercial.html', agences=agences)
from flask import Blueprint, render_template, session, redirect, url_for
from database import Database
from models.agence import AgenceRepository
from models.bien import BienRepository

agence_bp = Blueprint('agence', __name__)
db_manager = Database()

@agence_bp.route('/')
def index_root():
    return redirect(url_for('agence.accueil'))

@agence_bp.route('/agences')
def agences_alias():
    return redirect(url_for('agence.accueil'))

@agence_bp.route('/agence')
def agence_alias():
    return redirect(url_for('agence.accueil'))

@agence_bp.route('/accueil')
def accueil():
    conn = db_manager.get_connection()
    repo_agence = AgenceRepository(conn)
    
    agences = repo_agence.find_all()
    top_agences = repo_agence.get_top_5_agences_favoris()
    conn.close()

    # Définition de la bannière (Première agence par défaut ou selon critères)
    banner_agence = agences[0] if agences else None

    return render_template(
        'accueil.html',
        agences=agences,
        top_agences=top_agences,
        banner_agence=banner_agence
    )

@agence_bp.route('/agence/<int:id_agence>')
def agence_detail(id_agence):
    role = session.get('role')
    conn = db_manager.get_connection()
    repo_agence = AgenceRepository(conn)
    repo_bien = BienRepository(conn)

    agence_obj = repo_agence.get_by_id(id_agence)
    if not agence_obj:
        conn.close()
        return 'Agence non trouvée', 404

    # On extrait les biens rattachés à cette agence en exclusivité
    biens = repo_bien.find_all_by_agence(id_agence)
    conn.close()

    return render_template(
        'agence_detail.html',
        agence=agence_obj,
        biens=biens,
        role=role
    )
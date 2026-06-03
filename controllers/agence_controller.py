from flask import Blueprint, render_template, session, redirect, url_for
from database import Database
from models.agence import AgenceRepository
from models.bien import BienRepository

agence_bp = Blueprint('agence', __name__)
db_manager = Database()

@agence_bp.route('/')
@agence_bp.route('/agences')
def liste_agences():
    conn = db_manager.get_connection()
    repo = AgenceRepository(conn)
    agences = repo.find_all()
    conn.close()
    return render_template('agences.html', agences=agences)

@agence_bp.route('/agence/<int:id_agence>')
def agence_detail(id_agence):
    session['selected_agence'] = id_agence
    conn = db_manager.get_connection()
    
    repo_agence = AgenceRepository(conn)
    repo_bien = BienRepository(conn)
    
    agence_obj = repo_agence.get_by_id(id_agence)
    if not agence_obj:
        conn.close()
        return "Agence non trouvée", 404
        
    biens = repo_bien.find_all_by_agence(id_agence)
    conn.close()
    
    return render_template('agence_detail.html', agence=agence_obj, biens=biens)
from flask import Blueprint, render_template, session, redirect, url_for, request
from database import Database
from models.agence import AgenceRepository
from models.bien import BienRepository

agence_bp = Blueprint('agence', __name__)
db_manager = Database()

# --- 1. PAGES D'ENTRÉE (SANS NAVBAR) ---
@agence_bp.route('/')
def index_root():
    return redirect(url_for('agence.selection_agence'))

@agence_bp.route('/ymmo')
def ymmo_alias():
    return redirect(url_for('agence.selection_agence'))

@agence_bp.route('/agences')
def agences_alias():
    return redirect(url_for('agence.selection_agence'))

@agence_bp.route('/agence')
def agence_alias():
    return redirect(url_for('agence.selection_agence'))

@agence_bp.route('/selection_agence')
def selection_agence():
    # Page d'entrée brute qui liste toutes les agences pour faire un choix
    conn = db_manager.get_connection()
    repo_agence = AgenceRepository(conn)
    agences = repo_agence.find_all()
    conn.close()
    return render_template('selection_agence.html', agences=agences)

@agence_bp.route('/choisir_agence/<int:id_agence>')
def choisir_agence(id_agence):
    # Action qui mémorise l'agence choisie et redirige vers /accueil
    session['selected_agence_id'] = id_agence
    return redirect(url_for('agence.accueil'))


# --- 2. PAGE D'ACCUEIL DE L'AGENCE SÉLECTIONNÉE (AVEC NAVBAR) ---
@agence_bp.route('/accueil')
def accueil():
    id_agence = session.get('selected_agence_id')
    
    # Si l'utilisateur tape /accueil sans avoir choisi d'agence au début, on le renvoie à la sélection
    if not id_agence:
        return redirect(url_for('agence.selection_agence'))
        
    conn = db_manager.get_connection()
    repo_agence = AgenceRepository(conn)
    
    # Récupérer l'agence choisie pour le Banner
    agence_choisie = repo_agence.get_by_id(id_agence)
    if not agence_choisie:
        session.pop('selected_agence_id', None)
        return redirect(url_for('agence.selection_agence'))
        
    # Calculer le Top 5 des biens DE CETTE AGENCE les plus présents dans les favoris
    with conn.cursor() as cur:
        cur.execute("""
            SELECT b.*, COUNT(f.id_favoris) as nb_favoris
            FROM bien b
            LEFT JOIN favoris f ON b.id_bien = f.id_bien
            WHERE b.id_agence = %s AND b.statut = 'Disponible'
            GROUP BY b.id_bien
            ORDER BY nb_favoris DESC
            LIMIT 5
        """, (id_agence,))
        # Transformation des dictionnaires SQL en objets Bien
        from models.bien import Bien
        columns = [desc[0] for desc in cur.description]
        top_biens = []
        for row in cur.fetchall():
            row_dict = dict(zip(columns, row))
            row_dict.pop('nb_favoris', None) # Retire l'alias pour ne pas bloquer le constructeur
            top_biens.append(Bien(**row_dict))
            
    conn.close()
    
    return render_template(
        'accueil.html',
        agence=agence_choisie,
        top_biens=top_biens
    )

@agence_bp.route('/agence/<int:id_agence>')
def agence_detail(id_agence):
    conn = db_manager.get_connection()
    repo_agence = AgenceRepository(conn)
    repo_bien = BienRepository(conn)

    agence_obj = repo_agence.get_by_id(id_agence)
    if not agence_obj:
        conn.close()
        return 'Agence non trouvée', 404

    biens = repo_bien.find_all_by_agence(id_agence)
    conn.close()

    return render_template('agence_detail.html', agence=agence_obj, biens=biens)
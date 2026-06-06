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
        
    # NOUVELLE REQUÊTE : Sélectionne le Top 5 en complétant si nécessaire
    with conn.cursor() as cur:
        cur.execute("""
            SELECT b.*, COUNT(f.id_favoris) as nb_favoris
            FROM bien b
            LEFT JOIN favoris f ON b.id_bien = f.id_bien
            WHERE b.id_agence = %s AND b.statut = 'Disponible'
            GROUP BY b.id_bien
            ORDER BY nb_favoris DESC, b.id_bien DESC
            LIMIT 5
        """, (id_agence,))
        
        from models.bien import Bien
        columns = [desc[0] for desc in cur.description]
        top_biens = []
        for row in cur.fetchall():
            row_dict = dict(zip(columns, row))
            
            row_dict.pop('nb_favoris', None) 
            
            bien = Bien(**row_dict)
            
            cur.execute("SELECT image_url FROM photo_bien WHERE id_bien = %s", (bien.id_bien,))
            bien.images = [p['image_url'] for p in cur.fetchall()]
            
            top_biens.append(bien)
            
    conn.close()
    
    return render_template(
        'accueil.html',
        agence=agence_choisie,
        top_biens=top_biens
    )
    
    return render_template(
        'accueil.html',
        agence=agence_choisie,
        top_biens=top_biens
    )

@agence_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        pass
    return render_template('contact.html')

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

    with conn.cursor() as cur:
        for bien in biens:
            cur.execute("SELECT image_url FROM photo_bien WHERE id_bien = %s", (bien.id_bien,))
            bien.images = [p['image_url'] for p in cur.fetchall()]
    conn.close()

    return render_template('agence_detail.html', agence=agence_obj, biens=biens)
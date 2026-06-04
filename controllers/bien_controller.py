from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from database import Database
from models.bien import BienRepository
from models.carte import generer_carte_un_bien
from helpers.auth_helper import role_required
import os
from werkzeug.utils import secure_filename

bien_bp = Blueprint('bien', __name__)
db_manager = Database()

@bien_bp.route('/biens')
def liste_biens():
    id_agence = session.get('selected_agence_id')
    if not id_agence:
        flash("Veuillez d'abord sélectionner une agence.", "error")
        return redirect(url_for('agence.selection_agence'))

    ville = request.args.get('ville')
    prix_max = request.args.get('prix_max')
    type_bien = request.args.get('type_bien')
    nbr_chambres_min = request.args.get('nbr_chambres_min')
    type_chauffage = request.args.get('type_chauffage')
    etat_logement = request.args.get('etat_logement')
    avec_balcon = request.args.get('avec_balcon') == 'on'
    avec_parking = request.args.get('avec_parking') == 'on'
    avec_ascenseur = request.args.get('avec_ascenseur') == 'on'

    conn = db_manager.get_connection()
    repo = BienRepository(conn)
    
    biens = repo.find_by_filter(
        id_agence, ville, prix_max, type_bien, 
        nbr_chambres_min=nbr_chambres_min, 
        avec_balcon=avec_balcon, 
        avec_parking=avec_parking,
        type_chauffage=type_chauffage,
        avec_ascenseur=avec_ascenseur,
        etat_logement=etat_logement
    )
    conn.close()
    return render_template('listeBien.html', biens=biens)

@bien_bp.route('/bien/<int:id_bien>')
def detail_bien(id_bien):
    conn = db_manager.get_connection()
    repo = BienRepository(conn)
    bien = repo.get_by_id(id_bien)
    conn.close()
    if not bien:
        flash("Ce bien n'existe pas.", "error")
        return redirect(url_for('agence.liste_biens'))        
    return render_template('produit.html', bien=bien)

@bien_bp.route('/carte/<int:id_bien>')
def voir_carte_bien(id_bien):
    conn = db_manager.get_connection()
    repo = BienRepository(conn)
    bien_obj = repo.get_by_id(id_bien)
    conn.close()
    if not bien_obj:
        return "Bien introuvable", 404
               
    carte_html = generer_carte_un_bien(bien_obj)
    return render_template('carte_bien.html', bien=bien_obj, carte_html=carte_html)

# Définir les extensions autorisées
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bien_bp.route('/creation_bien', methods=['GET', 'POST'])
@role_required(['commercial'])
def creation_bien():
    if request.method == 'POST':
        conn = db_manager.get_connection()
        repo = BienRepository(conn)
        try:
            a_balcon = True if request.form.get('a_balcon') == 'on' else False
            a_parking = True if request.form.get('a_parking') == 'on' else False
            a_ascenseur = True if request.form.get('a_ascenseur') == 'on' else False

            annee = request.form.get('annee_construction')
            annee_val = int(annee) if annee and annee.strip() != "" else None

            id_bien = repo.create(
                ville=request.form.get('ville'),
                adresse=request.form.get('adresse'),
                description=request.form.get('description'),
                nbr_pieces=request.form.get('nbrPieces', type=int),
                surface=request.form.get('surface', type=float),
                type_bien=request.form.get('typeBien'),
                prix=request.form.get('prix', type=float),
                id_commercial=session.get('id_commercial'),
                id_agence=session.get('id_agence'),
                nbr_chambres=request.form.get('nbrChambres', default=0, type=int),
                a_balcon=a_balcon,
                a_parking=a_parking,
                type_chauffage=request.form.get('type_chauffage'),
                etage=request.form.get('etage'),
                a_ascenseur=a_ascenseur,
                etat_logement=request.form.get('etat_logement'),
                annee_construction=annee_val
            )
            
            if 'photos' in request.files:
                files = request.files.getlist('photos')
                upload_folder = os.path.join('static', 'uploads')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        unique_filename = f"bien_{id_bien}_{filename}"
                        file_path = os.path.join(upload_folder, unique_filename)
                        file.save(file_path)
                        web_path = f"static/uploads/{unique_filename}"
                        repo.add_photo(id_bien, web_path)

            flash("Le bien ainsi que ses illustrations ont été publiés avec succès !", "success")
            return redirect(url_for('agence.agence_detail', id_agence=session.get('id_agence')))
        except Exception as e:
            conn.rollback()
            flash(f"Erreur lors de l'ajout : {e}", "error")
        finally:
            conn.close()
    return render_template('miseEnVente.html')


@bien_bp.route('/bien/<int:id_bien>/supprimer', methods=['POST'])
@role_required(['commercial', 'admin'])
def supprimer_bien(id_bien):
    conn = db_manager.get_connection()
    repo = BienRepository(conn)
    bien_obj = repo.get_by_id(id_bien)
          
    if not bien_obj:
        conn.close()
        flash("Bien introuvable.", "error")
        return redirect(url_for('agence.accueil'))
              
    if session.get('role') == 'commercial' and session.get('id_agence') != bien_obj.id_agence:
        conn.close()
        flash("Action non autorisée sur les biens d'une autre agence.", "error")
        return redirect(url_for('agence.accueil'))
              
    repo.delete(id_bien)
    conn.close()
    flash("Le bien a été supprimé avec succès.", "success")
    return redirect(url_for('agence.agence_detail', id_agence=bien_obj.id_agence))

@bien_bp.route('/bien/<int:id_bien>/add_favoris', methods=['POST'])
@role_required(['client'])
def ajouter_favoris(id_bien):
    conn = db_manager.get_connection()
    repo = BienRepository(conn)
    repo.add_favoris(session.get('id_client'), id_bien)
    conn.close()
    flash("Bien ajouté à vos favoris !", "success")
    return redirect(url_for('bien.bien_detail', id_bien=id_bien))

@bien_bp.route('/bien/<int:id_bien>/remove_favoris', methods=['POST'])
@role_required(['client'])
def retirer_favoris(id_bien):
    conn = db_manager.get_connection()
    repo = BienRepository(conn)
    repo.remove_favoris(session.get('id_client'), id_bien)
    conn.close()
    flash("Bien retiré de vos favoris.", "info")
    return redirect(url_for('auth.voir_profil'))
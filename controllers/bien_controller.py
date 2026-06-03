from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import Database
from models.bien import BienRepository
from helpers.auth_helper import role_required

bien_bp = Blueprint('bien', __name__)
db_manager = Database()

@bien_bp.route('/biens')
def liste_biens():
    ville = request.args.get('ville')
    prix_max = request.args.get('prix_max', type=float)
    type_bien = request.args.get('type_bien')

    conn = db_manager.get_connection()
    repo = BienRepository(conn)
    biens = repo.find_by_filter(ville, prix_max, type_bien)
    conn.close()
    return render_template('listeBien.html', biens=biens)

@bien_bp.route('/bien/<int:id_bien>')
def bien_detail(id_bien):
    conn = db_manager.get_connection()
    repo = BienRepository(conn)
    bien_obj = repo.get_by_id(id_bien)
    conn.close()
    if not bien_obj:
        return "Bien introuvable", 404
    return render_template('produit.html', bien=bien_obj)

@bien_bp.route('/bien/ajouter', methods=['GET', 'POST'])
@role_required(['commercial', 'admin'])
def ajouter_bien():
    if request.method == 'POST':
        conn = db_manager.get_connection()
        repo = BienRepository(conn)
        try:
            repo.create(
                ville=request.form.get('ville'),
                adresse=request.form.get('adresse'),
                description=request.form.get('description'),
                nbr_pieces=request.form.get('nbrPieces', type=int),
                surface=request.form.get('surface', type=float),
                type_bien=request.form.get('typeBien'),
                prix=request.form.get('prix', type=float),
                id_commercial=session.get('id_commercial'),
                id_agence=session.get('id_agence')
            )
            flash("Le bien a été publié avec succès !", "success")
            return redirect(url_for('agence.agence_detail', id_agence=session.get('id_agence')))
        except Exception as e:
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
        return redirect(url_for('agence.liste_agences'))

    # Sécurité : Un commercial ne peut supprimer que les biens de son agence
    if session.get('role') == 'commercial' and session.get('id_agence') != bien_obj.id_agence:
        conn.close()
        flash("Action non autorisée sur les biens d'une autre agence.", "error")
        return redirect(url_for('agence.liste_agences'))

    repo.delete(id_bien)
    conn.close()
    flash("Bien supprimé avec succès.", "success")
    return redirect(url_for('agence.agence_detail', id_agence=bien_obj.id_agence))
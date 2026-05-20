from flask import Flask, request, render_template, session, redirect, url_for, flash
from database import Database

# Imports de tous les Repositories (Modèles)
from models.utilisateur import UtilisateurRepository
from models.agence import AgenceRepository
from models.bien import BienRepository
from models.client import ClientRepository
from models.commercial import CommercialRepository
from models.favoris import FavorisRepository
from models.messagerie import MessagerieRepository
from models.file_discussion import FileDiscussionRepository
from models.photo import PhotoRepository
from models.piece import PieceRepository
from models.statistique import StatistiqueRepository
from models.transaction import TransactionRepository
from helpers.auth_helper import role_required

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ymmo'
db_manager = Database()


@app.route('/')
@app.route('/accueil')
def accueil():
    try:
        #from models.carte import generer_carte_biens
        #generer_carte_biens()
        
        conn = db_manager.get_connection()
        repo = AgenceRepository(conn)
        mes_agences = repo.find_all()
        conn.close()
        return render_template('accueil.html', agences=mes_agences)
    except Exception as e:
        return f"Erreur de base de données : {e}"


@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = db_manager.get_connection()
        user_repo = UtilisateurRepository(conn)
        commercial_repo = CommercialRepository(conn)
        
        if user_repo.verifieMdp(password, email):
            utilisateur = user_repo.get_by_email(email)
            
            session['user_id'] = utilisateur.id
            session['role'] = utilisateur.role
            
            if utilisateur.role == 'commercial':
                session['id_agence'] = commercial_repo.get_idAgence(utilisateur.id)
            else:
                session['id_agence'] = None
                
            conn.close()
            flash("Connexion réussie !", "success")
            return redirect(url_for('profil'))
        else:
            message = "Email ou mot de passe incorrect."
        conn.close()
        
    return render_template('connexion.html', message=message)


@app.route('/deconnexion')
def deconnexion():
    session.clear()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for('connexion'))


@app.route('/profil')
def profil():
    user_id = session.get('user_id')
    if not user_id:
        flash("Veuillez vous connecter pour accéder à votre profil.", "error")
        return redirect(url_for('connexion'))
        
    conn = db_manager.get_connection()
    repo = UtilisateurRepository(conn)
    utilisateur = repo.get_by_id(user_id)
    conn.close()
    return render_template('profil.html', utilisateur=utilisateur)


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    message = None
    conn = db_manager.get_connection()
    
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        role = request.form.get('role')
        id_agence = request.form.get('id_agence')
        
        user_repo = UtilisateurRepository(conn)
        
        try:
            user_repo.createUtilisateur(fname, lname, email, password, phone, role)
            
            nouvel_user = user_repo.get_by_email(email)
            
            if role == 'commercial':
                import random
                matricule_genere = f"MAT-{random.randint(1000, 9999)}"
                
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO commercial (date_embauche, matricule, id_agence, id_utilisateur)
                    VALUES (NOW(), %s, %s, %s)
                """, (matricule_genere, id_agence, nouvel_user.id))
                conn.commit()
                cur.close()
                
            elif role == 'client':
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO client (type_client, budget_max, id_agence, id_utilisateur)
                    VALUES ('Particulier', 0, NULL, %s)
                """, (nouvel_user.id,))
                conn.commit()
                cur.close()

            flash("Inscription réussie ! Vous pouvez maintenant vous connecter.", "success")
            conn.close()
            return redirect(url_for('connexion'))
            
        except Exception as e:
            message = f"Erreur lors de l'inscription : {e}"
    
    agence_repo = AgenceRepository(conn)
    toutes_les_agences = agence_repo.find_all()
    conn.close()
    
    return render_template('inscription.html', message=message, agences_dispo=toutes_les_agences)


@app.route('/agence')
@app.route('/agences')
def agence():
    try:
        conn = db_manager.get_connection()
        repo = AgenceRepository(conn)
        mes_agences = repo.find_all()
        conn.close()
        return render_template('agences.html', agences=mes_agences)
    except Exception as e:
        return f"Erreur de base de données : {e}"


@app.route('/bien')
def bien():
    try:
        ville = request.args.get('ville')
        prix_max = request.args.get('prix_max', type=float)
        type_bien = request.args.get('type_bien')
        
        conn = db_manager.get_connection()
        repo = BienRepository(conn)
        
        if not ville and not prix_max and not type_bien:
            mes_biens = repo.find_all()
        else:
            mes_biens = repo.find_by_filter(ville, prix_max, type_bien)
            
        conn.close()
        return render_template('listeBien.html', biens=mes_biens)
    except Exception as e:
        return f"Erreur de base de données : {e}"


@app.route('/bien/<int:id>')
def bien_detail(id):
    try:
        conn = db_manager.get_connection()
        
        bien_repo = BienRepository(conn)
        bien = bien_repo.getProduit(id)
        
        if not bien:
            conn.close()
            return "Bien non trouvé", 404
            
        piece_repo = PieceRepository(conn)
        mes_pieces = piece_repo.find_by_bien(id)
        
        stats_repo = StatistiqueRepository(conn)
        toutes_les_stats = stats_repo.find_all()
        
        stats_associees = None
        for s in toutes_les_stats:
            if s.zone_geographique.lower() == bien.ville.lower():
                stats_associees = s
                break
                
        conn.close()
        return render_template('produit.html', bien=bien, pieces=mes_pieces, statistiques=stats_associees)
    except Exception as e:
        return f"Erreur de base de données : {e}"


@app.route('/mise_en_vente', methods=['GET', 'POST'])
@role_required(['admin', 'commercial'])
def mise_en_vente():
    message = None
    if request.method == 'POST':
        ville = request.form.get('ville')
        adresse = request.form.get('adresse')
        description = request.form.get('description')
        nbrPieces = request.form.get('nbrPieces')
        surface = request.form.get('surface')
        typeBien = request.form.get('typeBien')
        exposition = request.form.get('exposition')
        etatLogement = request.form.get('etatLogement')
        energieChauffage = request.form.get('energieChauffage')
        typeEauChaude = request.form.get('typeEauChaude')
        typeChauffage = request.form.get('typeChauffage')
        moyenEauChaude = request.form.get('moyenEauChaude')
        etage = request.form.get('etage')
        vue = request.form.get('vue')
        prix = request.form.get('prix')
        statut = request.form.get('statut')
        agence = request.form.get('agence')
        
        conn = db_manager.get_connection()
        repo = BienRepository(conn)
        try:
            repo.createBien(ville, adresse, description, nbrPieces, surface, typeBien, 
                            exposition, etatLogement, energieChauffage, typeEauChaude, 
                            typeChauffage, moyenEauChaude, etage, vue, prix, statut, agence)
            flash("Mise en vente réussie !", "success")
            conn.close()
            return redirect(url_for('bien'))
        except Exception as e:
            message = f"Erreur lors de la mise en vente : {e}"
        conn.close()
        
    return render_template('miseEnVente.html', message=message)


@app.route('/bien/<int:id>/supprimer', methods=['POST'])
@role_required(['admin', 'commercial'])
def supprimer_bien(id):
    try:
        conn = db_manager.get_connection()
        repo = BienRepository(conn)
        
        bien_a_supprimer = repo.getProduit(id)
        if not bien_a_supprimer:
            conn.close()
            flash("Bien introuvable.", "error")
            return redirect(url_for('bien'))
            
        if session.get('role') == 'commercial' and session.get('id_agence') != bien_a_supprimer.id_agence:
            conn.close()
            flash("Action refusée : Ce bien n'appartient pas à la liste de votre agence.", "error")
            return redirect(url_for('bien'))

        repo.deleteBien(id)
        conn.close()
        
        flash("Le bien a été supprimé avec succès.", "success")
        return redirect(url_for('bien'))
    except Exception as e:
        return f"Erreur lors de la suppression : {e}"


@app.route('/messagerie')
def messagerie_boite():
    user_id = session.get('user_id')
    if not user_id:
        flash("Veuillez vous connecter pour voir vos messages.", "error")
        return redirect(url_for('connexion'))
        
    file_id = request.args.get('file_id', type=int)
    
    conn = db_manager.get_connection()
    file_repo = FileDiscussionRepository(conn)
    msg_repo = MessagerieRepository(conn)
    
    discussions = file_repo.find_all()
    
    active_file = None
    messages = []
    if file_id:
        for f in discussions:
            if f.id_file_discussion == file_id:
                active_file = f
                break
        messages = msg_repo.find_all(file_id)
        
    conn.close()
    return render_template('messagerie.html', discussions=discussions, active_file=active_file, messages=messages)


@app.route('/messagerie/creer')
def messagerie_creer():
    user_id = session.get('user_id')
    id_bien = request.args.get('id_bien', type=int)
    
    if not user_id:
        flash("Vous devez être connecté pour ouvrir un tchat agence.", "error")
        return redirect(url_for('connexion'))
        
    conn = db_manager.get_connection()
    file_repo = FileDiscussionRepository(conn)
    bien_repo = BienRepository(conn)
    
    bien = bien_repo.getProduit(id_bien)
    nom_discussion = f"Discussion Projet - Bien #{id_bien} ({bien.ville if bien else ''})"
    
    file_repo.create_file_discussion(nom_discussion, "NOW()")
    
    toutes_les_files = file_repo.find_all()
    dernier_id = toutes_les_files[-1].id_file_discussion if toutes_les_files else None
    
    conn.close()
    flash("Nouvelle conversation initiée !", "success")
    return redirect(f"/messagerie?file_id={dernier_id}")


@app.route('/messagerie/envoyer', methods=['POST'])
def messagerie_envoyer():
    user_id = session.get('user_id')
    role = session.get('role')
    id_file = request.form.get('id_file_discussion', type=int)
    contenu = request.form.get('contenu_message')
    
    if not user_id:
        return "Non autorisé", 401
        
    conn = db_manager.get_connection()
    msg_repo = MessagerieRepository(conn)
    
    id_commercial = user_id if role == 'commercial' else None
    id_client = user_id if role == 'client' else None
    
    msg_repo.create_message(contenu, id_commercial, id_client, id_file)
    conn.close()
    
    return redirect(f"/messagerie?file_id={id_file}")

@app.route('/utilisateurs')
@role_required(['admin']) # Seuls les admins peuvent déclencher cette fonction
def liste_utilisateurs():
    conn = db_manager.get_connection()
    repo = UtilisateurRepository(conn)
    tous_les_users = repo.find_all()
    conn.close()
    return render_template('utilisateur.html', utilisateurs=tous_les_users)

@app.route('/dashboard')
@role_required(['admin', 'commercial']) # Sécurité d'accès
def dashboard():
    try:
        conn = db_manager.get_connection()
        stats_repo = StatistiqueRepository(conn)
        stats_repo.calculer_real_stats_from_db()
        toutes_les_stats = stats_repo.find_all()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*), SUM(prix_final) FROM transaction")
        res_trans = cur.fetchone()
        total_ventes = res_trans[0] or 0
        ca_total = res_trans[1] or 0
        cur.execute("SELECT COUNT(*) FROM bien WHERE statut ILIKE 'Disponible'")
        biens_actifs = cur.fetchone()[0] or 0
        cur.close()
        conn.close()
        return render_template('dashboard_stats.html', 
                               statistiques=toutes_les_stats, 
                               total_ventes=total_ventes, 
                               ca_total=ca_total, 
                               biens_actifs=biens_actifs)
    except Exception as e:
        return f"Erreur lors de la génération du rapport statistique : {e}"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
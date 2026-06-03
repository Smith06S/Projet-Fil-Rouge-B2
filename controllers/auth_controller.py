from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import Database
from models.utilisateur import UtilisateurRepository
from models.bien import BienRepository
from helpers.auth_helper import role_required

auth_bp = Blueprint('auth', __name__)
db_manager = Database()

@auth_bp.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('lname')
        prenom = request.form.get('fname')
        email = request.form.get('email')
        password = request.form.get('password')
        telephone = request.form.get('phone')
        budget = request.form.get('budget', 0, type=float)
        conn = db_manager.get_connection()
        repo = UtilisateurRepository(conn)
        try:
            repo.create_client(nom, prenom, email, password, telephone, budget)
            flash("Inscription réussie, connectez-vous !", "success")
            return redirect(url_for('auth.connexion'))
        except Exception as e:
            conn.rollback()
            flash(f"Erreur d'inscription : {e}", "error")
        finally:
            conn.close()
    return render_template('inscription.html')

@auth_bp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = db_manager.get_connection()
        repo = UtilisateurRepository(conn)
        user = repo.get_by_email(email)
        if user and repo.verifier_password(password, user.mdp):
            session['user_id'] = user.id_utilisateur
            session['role'] = user.role
            session['nom_complet'] = f"{user.prenom} {user.nom}"
            if user.role == 'client':
                session['id_client'] = repo.get_client_id(user.id_utilisateur)
            elif user.role == 'commercial':
                comm = repo.get_commercial_details(user.id_utilisateur)
                session['id_commercial'] = comm['id_commercial']
                session['id_agence'] = comm['id_agence']
            conn.close()
            return redirect(url_for('agence.accueil'))
                 
        flash("Email ou mot de passe incorrect.", "error")
        conn.close()
    return render_template('connexion.html')

@auth_bp.route('/profil')
@role_required(['client', 'commercial', 'admin'])
def voir_profil():
    conn = db_manager.get_connection()
    repo_user = UtilisateurRepository(conn)
    repo_bien = BienRepository(conn)
         
    utilisateur = repo_user.get_by_id(session.get('user_id'))
    favoris = []
    if session.get('role') == 'client':
        favoris = repo_bien.get_favoris_by_client(session.get('id_client'))
             
    conn.close()
    return render_template('profil.html', utilisateur=utilisateur, favoris=favoris)

@auth_bp.route('/utilisateur/<int:id_utilisateur>/supprimer', methods=['POST'])
@role_required(['admin'])
def supprimer_utilisateur(id_utilisateur):
    if id_utilisateur == session.get('user_id'):
        flash("Vous ne pouvez pas supprimer votre propre compte.", "error")
        return redirect(url_for('dashboard.voir_dashboard'))
        
    conn = db_manager.get_connection()
    try:
        with conn.cursor() as cur:
            # La suppression se propage en cascade sur les tables enfants via les FK sql
            cur.execute("DELETE FROM utilisateur WHERE id_utilisateur = %s", (id_utilisateur,))
        conn.commit()
        flash("L'utilisateur a été supprimé définitivement du système.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Erreur lors de la suppression : {e}", "error")
    finally:
        conn.close()
        
    return redirect(url_for('dashboard.voir_dashboard'))

@auth_bp.route('/deconnexion')
def deconnexion():
    session.clear()
    flash("Déconnexion réussie.", "info")
    return redirect(url_for('auth.connexion'))
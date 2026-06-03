from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import Database
from models.utilisateur import UtilisateurRepository

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
            return redirect(url_for('agence.liste_agences'))
        
        flash("Email ou mot de passe incorrect.", "error")
        conn.close()
    return render_template('connexion.html')

@auth_bp.route('/deconnexion')
def deconnexion():
    session.clear()
    flash("Déconnexion réussie.", "info")
    return redirect(url_for('auth.connexion'))
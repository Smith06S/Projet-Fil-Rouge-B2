from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import Database

app = Flask(__name__)
app.secret_key = 'ymmo_secret_key_123'  # Nécessaire pour les sessions et messages flash

db = Database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/accueil')
def accueil():
    return render_template('accueil.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        mot_de_passe = request.form.get('password')
        role = request.form.get('role', 'client')
        
        if not nom or not email or not mot_de_passe:
            flash("Veuillez remplir tous les champs obligatoires.", "danger")
            return render_template('inscription.html')
            
        # Modifie ici selon les vraies colonnes de ta table utilisateur si besoin
        query = "INSERT INTO utilisateur (nom, prenom, email, mot_de_passe, role) VALUES (%s, %s, %s, %s, %s);"
        try:
            db.execute_query(query, (nom, prenom, email, mot_de_passe, role))
            flash("Inscription réussie ! Connectez-vous.", "success")
            return redirect(url_for('connexion'))
        except Exception as e:
            flash(f"Erreur lors de l'inscription : {e}", "danger")
            
    return render_template('inscription.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form.get('email')
        mot_de_passe = request.form.get('password')
        
        query = "SELECT id_utilisateur, nom, prenom, role FROM utilisateur WHERE email = %s AND mot_de_passe = %s;"
        try:
            user = db.fetch_one(query, (email, mot_de_passe))
            if user:
                session['user_id'] = user['id_utilisateur']
                session['user_nom'] = user['nom']
                session['user_prenom'] = user['prenom']
                session['user_role'] = user['role']
                flash(f"Ravi de vous revoir, {user['prenom']} !", "success")
                return redirect(url_for('accueil'))
            else:
                flash("Identifiants incorrects.", "danger")
        except Exception as e:
            # Si ta table utilisateur utilise des structures différentes
            query_alt = "SELECT * FROM utilisateur WHERE email = %s AND mot_de_passe = %s;"
            try:
                user = db.fetch_one(query_alt, (email, mot_de_passe))
                if user:
                    # Tente de récupérer dynamiquement l'id
                    session['user_id'] = user.get('id_utilisateur') or user.get('idutilisateur') or list(user.values())[0]
                    session['user_nom'] = user.get('nom', '')
                    session['user_prenom'] = user.get('prenom', '')
                    session['user_role'] = user.get('role', 'client')
                    return redirect(url_for('accueil'))
            except Exception:
                flash(f"Erreur de connexion BDD : {e}", "danger")
            
    return render_template('connexion.html')

@app.route('/deconnexion')
def deconnexion():
    session.clear()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for('index'))

@app.route('/biens')
def liste_biens():
    # Sélection des colonnes validées par ta commande psql
    query = "SELECT id_bien, prix, description, ville, type_bien, nbr_pieces, surface FROM bien;"
    biens_data = db.fetch_all(query)
    return render_template('listeBien.html', biens=biens_data)

@app.route('/bien/<int:id>')
def produit(id):
    query = "SELECT id_bien, prix, description, ville, type_bien, nbr_pieces, surface, adresse, exposition, etat_logement, vue FROM bien WHERE id_bien = %s;"
    bien = db.fetch_one(query, (id,))
    if not bien:
        flash("Ce bien n'existe pas.", "warning")
        return redirect(url_for('liste_biens'))
    return render_template('produit.html', bien=bien)

@app.route('/mise-en-vente', methods=['GET', 'POST'])
def mise_en_vente():
    if 'user_id' not in session:
        flash("Vous devez être connecté pour publier une annonce.", "warning")
        return redirect(url_for('connexion'))
        
    if request.method == 'POST':
        ville = request.form.get('ville')
        adresse = request.form.get('adresse', 'Non spécifiée')
        description = request.form.get('description')
        nbr_pieces = request.form.get('nbr_pieces', 1)
        surface = request.form.get('surface', 0)
        type_bien = request.form.get('type_bien')
        prix = request.form.get('prix')
        
        # Valeurs par défaut exigées par tes contraintes "not null" de la table
        exposition = request.form.get('exposition', 'Standard')
        etat_logement = request.form.get('etat_logement', 'Bon état')
        energie_chauffage = request.form.get('energie_chauffage', 'Électrique')
        type_eau_chaude = request.form.get('type_eau_chaude', 'Individuel')
        type_chauffage = request.form.get('type_chauffage', 'Individuel')
        moyen_eau_chaude = request.form.get('moyen_eau_chaude', 'Ballon')
        etage = request.form.get('etage', 'Rez-de-chaussée')
        vue = request.form.get('vue', 'Dégagée')
        statut = request.form.get('statut', 'Disponible')
        id_agence = request.form.get('id_agence', 1) # Assigne par défaut à l'agence 1
        
        query = """
            INSERT INTO bien (ville, adresse, description, nbr_pieces, surface, type_bien, exposition, 
            etat_logement, energie_chauffage, type_eau_chaude, type_chauffage, moyen_eau_chaude, etage, vue, prix, statut, id_agence) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            db.execute_query(query, (ville, adresse, description, nbr_pieces, surface, type_bien, exposition, 
                                     etat_logement, energie_chauffage, type_eau_chaude, type_chauffage, moyen_eau_chaude, etage, vue, prix, statut, id_agence))
            flash("Votre bien a été mis en vente !", "success")
            return redirect(url_for('liste_biens'))
        except Exception as e:
            flash(f"Erreur d'insertion dans la table bien : {e}", "danger")
            
    return render_template('miseEnVente.html')

@app.route('/agences')
def agences():
    return render_template('agences.html')

@app.route('/profil')
def profil():
    if 'user_id' not in session:
        return redirect(url_for('connexion'))
    return render_template('profil.html')

@app.route('/messagerie')
def messagerie():
    if 'user_id' not in session:
        return redirect(url_for('connexion'))
    return render_template('messagerie.html')

@app.route('/dashboard')
def dashboard_stats():
    return render_template('dashboard_stats.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import Database

app = Flask(__name__)
app.secret_key = 'ymmo_secret_key_123'

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
            
        query = "INSERT INTO utilisateur (nom, prenom, email, mot_de_passe, role) VALUES (%s, %s, %s, %s, %s);"
        try:
            db.execute_query(query, (nom, prenom, email, mot_de_passe, role))
            flash("Inscription réussie ! Connectez-vous.", "success")
            return redirect(url_for('connexion'))
        except Exception as e:
            flash(f"Erreur d'inscription : {e}", "danger")
            
    return render_template('inscription.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form.get('email')
        mot_de_passe = request.form.get('password')
        
        query = "SELECT id_utilisateur, nom, prenom, role FROM utilisateur WHERE email = %s AND mot_de_passe = %s;"
        user = db.fetch_one(query, (email, mot_de_passe))
        
        if user:
            session['user_id'] = user[0]
            session['user_nom'] = user[1]
            session['user_prenom'] = user[2]
            session['user_role'] = user[3]
            flash(f"Ravi de vous revoir, {user[2]} !", "success")
            return redirect(url_for('accueil'))
        else:
            flash("Identifiants incorrects.", "danger")
            
    return render_template('connexion.html')

@app.route('/deconnexion')
def deconnexion():
    session.clear()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for('index'))

@app.route('/biens')
def liste_biens():
    # Récupération de l'ensemble des colonnes dans l'ordre de ta table
    query = "SELECT id_bien, ville, adresse, description, nbr_pieces, surface, type_bien, prix FROM bien;"
    biens_data = db.fetch_all(query)
    return render_template('listeBien.html', biens=biens_data)

@app.route('/bien/<int:id>')
def produit(id):
    query = "SELECT id_bien, ville, adresse, description, nbr_pieces, surface, type_bien, prix FROM bien WHERE id_bien = %s;"
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
        
        query = """
            INSERT INTO bien (ville, adresse, description, nbr_pieces, surface, type_bien, exposition, 
            etat_logement, energie_chauffage, type_eau_chaude, type_chauffage, moyen_eau_chaude, etage, vue, prix, statut, id_agence) 
            VALUES (%s, %s, %s, %s, %s, %s, 'Standard', 'Bon état', 'Électrique', 'Individuel', 'Individuel', 'Ballon', '1', 'Dégagée', %s, 'Disponible', 1);
        """
        try:
            db.execute_query(query, (ville, adresse, description, nbr_pieces, surface, type_bien, prix))
            flash("Votre bien a été mis en vente !", "success")
            return redirect(url_for('liste_biens'))
        except Exception as e:
            flash(f"Erreur lors de l'ajout : {e}", "danger")
            
    return render_template('miseEnVente.html')

@app.route('/agences')
def agences():
    return render_template('agences.html')

@app.route('/profil')
def profil():
    return render_template('profil.html')

@app.route('/messagerie')
def messagerie():
    return render_template('messagerie.html')

@app.route('/dashboard')
def dashboard_stats():
    return render_template('dashboard_stats.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
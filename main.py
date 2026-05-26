from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import Database

app = Flask(__name__)
app.secret_key = 'ymmo_secret_key_123'  # Clé obligatoire pour les sessions et messages flash

# Initialisation de la base de données
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
            flash(f"Erreur lors de l'inscription : {e}", "danger")
            
    return render_template('inscription.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form.get('email')
        mot_de_passe = request.form.get('password')
        
        # Adaptation aux minuscules standards de PostgreSQL pour l'utilisateur
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
    # Correction stricte selon l'indication de Postgres (id_bien, prix_bien, etc.)
    query = "SELECT id_bien, prix_bien, description_bien, ville_bien, type_bien FROM bien;"
    biens_data = db.fetch_all(query)
    return render_template('listeBien.html', biens=biens_data)

@app.route('/bien/<int:id>')
def produit(id):
    query = "SELECT id_bien, prix_bien, description_bien, ville_bien, type_bien FROM bien WHERE id_bien = %s;"
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
        description = request.form.get('description')
        prix = request.form.get('prix')
        ville = request.form.get('ville')
        type_bien = request.form.get('type_bien')
        
        query = """
            INSERT INTO bien (prix_bien, description_bien, ville_bien, type_bien, id_utilisateur) 
            VALUES (%s, %s, %s, %s, %s);
        """
        try:
            db.execute_query(query, (prix, description, ville, type_bien, session['user_id']))
            flash("Votre bien a été mis en vente avec succès !", "success")
            return redirect(url_for('liste_biens'))
        except Exception as e:
            flash(f"Erreur lors de l'ajout : {e}", "danger")
            
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
    if 'user_id' not in session or session.get('user_role') != 'commercial':
        flash("Accès réservé aux agents commerciaux.", "danger")
        return redirect(url_for('accueil'))
    return render_template('dashboard_stats.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
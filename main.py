from flask import Flask, request, render_template
from database import Database
from models.utilisateur import UtilisateurRepository
from models.agence import AgenceRepository
from models.bien import BienRepository
from models.client import ClientRepository
from models.commercial import CommercialRepository
from models.favoris import FavorisRepository
from models.messagerie import MessagerieRepository
from models.photo import PhotoRepository
from models.piece import PieceRepository
from models.statistique import StatistiqueRepository
from models.transaction import TransactionRepository
from models.utilisateur import UtilisateurRepository

app = Flask(__name__)
db_manager = Database()

@app.route('/')
def index():
    try:
        conn = db_manager.get_connection()
        repo = UtilisateurRepository(conn)

        # On récupère la liste d'objets
        mes_utilisateurs = repo.find_all()

        conn.close()
        return render_template('utilisateur.html', utilisateurs=mes_utilisateurs)
    except Exception as e:
        return f"Erreur de base de données : {e}"

    

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = db_manager.get_connection()
        repo = UtilisateurRepository(conn)
        if repo.verifieMdp(password, email):
            message = "Connexion réussie !"
        else:
            message = "Email ou mot de passe incorrect."
        conn.close()
    return render_template('connexion.html', message=message)


@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    message = None
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        role = request.form.get('role')
        conn = db_manager.get_connection()
        repo = UtilisateurRepository(conn)
        try:
            repo.createUtilisateur(fname, lname, email, password, phone, role)
            message = "Inscription réussie ! Vous pouvez maintenant vous connecter."
        except Exception as e:
            message = f"Erreur lors de l'inscription : {e}"
        conn.close()
    return render_template('inscription.html', message=message)

@app.route('/agence')
def agence():
    try:
        conn = db_manager.get_connection()
        repo = AgenceRepository(conn)

        # On récupère la liste d'objets
        mes_agence = repo.find_all()

        conn.close()
        return render_template('agences.html', agences=mes_agence)
    except Exception as e:
        return f"Erreur de base de données : {e}"
    
@app.route('/bien')
def bien():
    try:
        conn = db_manager.get_connection()
        repo = BienRepository(conn)

        # On récupère la liste d'objets
        mes_biens = repo.find_all()

        conn.close()
        return render_template('listeBien.html', biens=mes_biens)
    except Exception as e:
        return f"Erreur de base de données : {e}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

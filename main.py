from flask import Flask, render_template
from database import Database
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

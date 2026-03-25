from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Fonction pour se connecter à ta base
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="ymmodb",
        user="postgres",
        password="ymmo123"
    )

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # On récupère toutes les données de la table 'users'
        cur.execute("SELECT * FROM utilisateur;")
        rows = cur.fetchall()

        # On récupère dynamiquement les noms des colonnes
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        conn.close()

        # On envoie les données au fichier HTML
        return render_template('index.html', columns=colnames, data=rows)
    except Exception as e:
        # Si une erreur survient, elle s'affichera sur la page web
        return f"<h1>Erreur de connexion SQL</h1><p>{e}</p>"

if __name__ == '__main__':
    # On écoute sur le port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)

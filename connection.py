from flask import Flask, request, render_template
from database import Database

app = Flask(__name__)
db_manager = Database()

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Username: {email}, Password: {password}")
    return render_template('connexion.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

'''
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

if bcrypt.checkpw(password, hashed):
    print("It Matches!")
else:
    print("It Does not Match :(")
'''

'''
SELECT * FROM utilisateur;

INSERT INTO utilisateur (email, nom, prenom, mdp, telephone, role)
VALUES ('sara@gmail.com', 'sara', 'smith', 'sara1234', '0632104556', 'client');
'''
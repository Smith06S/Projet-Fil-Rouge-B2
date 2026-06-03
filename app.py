from flask import Flask, redirect, url_for
from controllers.auth_controller import auth_bp
from controllers.agence_controller import agence_bp
from controllers.bien_controller import bien_bp
from controllers.chat_controller import chat_bp
from controllers.dashboard_controller import dashboard_bp

app = Flask(__name__)
app.secret_key = 'ymmo_secure_secret_key_b2'

app.register_blueprint(auth_bp)
app.register_blueprint(agence_bp)
app.register_blueprint(bien_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def index():
    return redirect(url_for('agence.liste_agences'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
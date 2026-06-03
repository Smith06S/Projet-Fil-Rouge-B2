from functools import wraps
from flask import session, flash, redirect, url_for

def role_required(allowed_roles=[]):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash("Veuillez vous connecter pour accéder à cette page.", "error")
                return redirect(url_for('auth.connexion'))
                
            if session.get('role') not in allowed_roles:
                flash("Accès refusé : Vous n'avez pas les permissions nécessaires.", "error")
                return redirect(url_for('agence.selection_agence'))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
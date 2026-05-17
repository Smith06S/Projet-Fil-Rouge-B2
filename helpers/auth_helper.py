from functools import wraps
from flask import session, redirect, url_for, flash

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs) :
            if 'role' not in session or session['role'] not in allowed_roles:
                flash("Accès refusé. Vous n'avez pas les permissions nécessaires.", "error")
                return redirect(url_for('connexion'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
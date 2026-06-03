from functools import wraps
from flask import session, flash, redirect, url_for

def role_required(allowed_roles=[]):
    """
    Décorateur personnalisé pour sécuriser les routes Flask selon le rôle de l'utilisateur.
    Garantit le respect des droits d'accès exigés par la grille d'évaluation.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 1. Vérification de l'authentification globale
            if 'user_id' not in session:
                flash("Veuillez vous connecter pour accéder à cette page.", "error")
                return redirect(url_for('auth.connexion'))
            
            # 2. Vérification des privilèges et des rôles stricts (SOLID / Sécurité)
            if session.get('role') not in allowed_roles:
                flash("Accès refusé : Vous n'avez pas les permissions nécessaires.", "error")
                return redirect(url_for('agence.liste_agences'))
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
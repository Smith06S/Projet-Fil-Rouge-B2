from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import Database
from models.messagerie import MessagerieRepository
from models.bien import BienRepository
from helpers.auth_helper import role_required

chat_bp = Blueprint('chat', __name__)
db_manager = Database()

@chat_bp.route('/messagerie')
@role_required(['client', 'commercial']) # L'admin n'est plus présent ici
def boite_reception():
    conn = db_manager.get_connection()
    repo = MessagerieRepository(conn)
          
    sub_id = session.get('id_client') if session.get('role') == 'client' else session.get('id_commercial')
    discussions = repo.get_discussions_by_user(session.get('user_id'), session.get('role'), sub_id)
          
    active_discussion_id = request.args.get('discussion_id', type=int)
    messages = []
    active_discussion = None
          
    if active_discussion_id:
        active_discussion = repo.get_discussion_by_id(active_discussion_id)
        if active_discussion:
            messages = repo.get_messages_by_discussion(active_discussion_id)
                  
    conn.close()
    return render_template('messagerie.html', discussions=discussions, active_discussion=active_discussion, messages=messages)

@chat_bp.route('/messagerie/initier/<int:id_bien>')
@role_required(['client'])
def initier_tchat(id_bien):
    conn = db_manager.get_connection()
    repo_bien = BienRepository(conn)
    repo_chat = MessagerieRepository(conn)
          
    bien = repo_bien.get_by_id(id_bien)
    if not bien:
        conn.close()
        return "Bien introuvable", 404
    discussion_existante = repo_chat.find_existing_discussion(id_bien, session.get('id_client'))
    if discussion_existante:
        conn.close()
        return redirect(url_for('chat.boite_reception', discussion_id=discussion_existante.id_discussion))
    titre = f"Discussion - {bien.type_bien} à {bien.ville}"
    id_disc = repo_chat.create_discussion(titre, id_bien, session.get('id_client'), bien.id_commercial)
    conn.close()
    return redirect(url_for('chat.boite_reception', discussion_id=id_disc))

@chat_bp.route('/messagerie/envoyer/<int:id_discussion>', methods=['POST'])
@role_required(['client', 'commercial'])
def envoyer_message(id_discussion):
    message_texte = request.form.get('contents_message')
    if message_texte:
        conn = db_manager.get_connection()
        repo = MessagerieRepository(conn)
        repo.save_message(message_texte, id_discussion, session.get('user_id'))
        conn.close()
    return redirect(url_for('chat.boite_reception', discussion_id=id_discussion))
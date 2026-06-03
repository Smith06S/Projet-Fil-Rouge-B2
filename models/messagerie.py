class Discussion:
    def __init__(self, id_discussion, titre, date_creation, id_bien, id_client, id_commercial):
        self.id_discussion = id_discussion
        self.titre = titre
        self.date_creation = date_creation
        self.id_bien = id_bien
        self.id_client = id_client
        self.id_commercial = id_commercial

class Message:
    def __init__(self, id_message, message, date_heure, id_discussion, id_expediteur, nom=None, prenom=None):
        self.id_message = id_message
        self.message = message
        self.date_heure = date_heure
        self.id_discussion = id_discussion
        self.id_expediteur = id_expediteur
        self.nom = nom
        self.prenom = prenom


class MessagerieRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def find_existing_discussion(self, id_bien, id_client):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM discussion WHERE id_bien = %s AND id_client = %s", (id_bien, id_client))
            row = cur.fetchone()
            return Discussion(**row) if row else None

    def create_discussion(self, titre, id_bien, id_client, id_commercial):
        with self.db.cursor() as cur:
            cur.execute("""INSERT INTO discussion (titre, id_bien, id_client, id_commercial) VALUES (%s, %s, %s, %s) RETURNING id_discussion""", (titre, id_bien, id_client, id_commercial))
            id_disc = cur.fetchone()['id_discussion']
        self.db.commit()
        return id_disc

    def get_messages_by_discussion(self, id_discussion):
        with self.db.cursor() as cur:
            cur.execute("""
                SELECT m.*, u.nom, u.prenom 
                FROM message m 
                JOIN utilisateur u ON m.id_expediteur = u.id_utilisateur
                WHERE m.id_discussion = %s 
                ORDER BY m.date_heure ASC
            """, (id_discussion,))
            return [Message(**row) for row in cur.fetchall()]

    def save_message(self, message, id_discussion, id_expediteur):
        with self.db.cursor() as cur:
            cur.execute("""INSERT INTO message (message, id_discussion, id_expediteur) VALUES (%s, %s, %s)""", (message, id_discussion, id_expediteur))
        self.db.commit()

    def get_discussions_by_user(self, user_id, role, sub_id):
        with self.db.cursor() as cur:
            if role == 'client':
                cur.execute("SELECT * FROM discussion WHERE id_client = %s", (sub_id,))
            elif role == 'commercial':
                cur.execute("SELECT * FROM discussion WHERE id_commercial = %s", (sub_id,))
            else:
                return []
            return [Discussion(**row) for row in cur.fetchall()]

    def get_discussion_by_id(self, id_discussion):
        with self.db.cursor() as cur:
            cur.execute("SELECT * FROM discussion WHERE id_discussion = %s", (id_discussion,))
            row = cur.fetchone()
            return Discussion(**row) if row else None

    # --- AJOUT DE LA SUPPRESSION DU CHAT ---
    def delete_discussion(self, id_discussion):
        with self.db.cursor() as cur:
            cur.execute("DELETE FROM discussion WHERE id_discussion = %s", (id_discussion,))
        self.db.commit()
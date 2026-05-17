class Messagerie:
    """Représente une messagerie (Entité)"""
    def __init__(self, id_messagerie, message, date_heure, id_commercial, id_client, id_file_discussion):
        self.id_messagerie = id_messagerie
        self.message = message
        self.date_heure = date_heure
        self.id_commercial = id_commercial
        self.id_client = id_client
        self.id_file_discussion = id_file_discussion

class MessagerieRepository:
    """Gère la communication avec la table 'messagerie'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all(self, id_file_discussion):
        cur = self.db.cursor()
        cur.execute("SELECT id_messagerie, message, date_heure, id_commercial, id_client FROM messagerie WHERE id_file_discussion = %s", (id_file_discussion,))
        rows = cur.fetchall()
        messageries = [Messagerie(r[0], r[1], r[2], r[3], r[4]) for r in rows]
        cur.close()
        return messageries
    
    def edit_message(self, id_messagerie, message, date_heure):        
        cur = self.db.cursor()
        cur.execute("""
            UPDATE messagerie 
            SET message = %s, date_heure = %s 
            WHERE id_messagerie = %s;
        """, (message, date_heure, id_messagerie))
        self.db.commit()
        cur.close()

    def create_message(self, message, id_commercial, id_client, id_file_discussion):
        cur = self.db.cursor()
        cur.execute("""
            INSERT INTO messagerie (message, date_heure, id_commercial, id_client, id_file_discussion) 
            VALUES (%s, NOW(), %s, %s, %s)
        """, (message, id_commercial, id_client, id_file_discussion))
        self.db.commit()
        cur.close()
        

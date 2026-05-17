class Messagerie:
    def __init__(self, id_message, message, date_heure, id_commercial, id_client):
        self.id_messagerie = id_message
        self.message = message
        self.date_heure = date_heure
        self.id_commercial = id_commercial
        self.id_client = id_client

class MessagerieRepository:
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all(self, id_file_discussion):
        cur = self.db.cursor()
        cur.execute("""
            SELECT id_message, message, date_heure, id_commercial, id_client 
            FROM message 
            WHERE id_file_discussion = %s
        """, (id_file_discussion,))
        rows = cur.fetchall()
        messageries = [Messagerie(r[0], r[1], r[2], r[3], r[4]) for r in rows]
        cur.close()
        return messageries

    def create_message(self, message, id_commercial, id_client, id_file_discussion):
        cur = self.db.cursor()
        cur.execute("""
            INSERT INTO message (message, date_heure, id_commercial, id_client, id_file_discussion) 
            VALUES (%s, NOW(), %s, %s, %s)
        """, (message, id_commercial, id_client, id_file_discussion))
        self.db.commit()
        cur.close()

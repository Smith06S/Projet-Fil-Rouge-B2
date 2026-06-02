class FileDiscussion:
    """Représente une agence (Entité)"""
    def __init__(self, id_file_discussion, nom_discussione, date_creation, id_bien=None):
        self.id_file_discussion = id_file_discussion
        self.nom_discussione = nom_discussione
        self.date_creation = date_creation
        self.id_bien = id_bien

class FileDiscussionRepository:
    """Gère la communication avec la table 'file discussion'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all(self):
        cur = self.db.cursor()
        cur.execute("SELECT id_file_discussion, nom_discussione, date_creation, id_bien FROM file_discussion")
        rows = cur.fetchall()

        file_discussions = [FileDiscussion(r[0], r[1], r[2], r[3]) for r in rows]

        cur.close()
        return file_discussions

    def create_file_discussion(self, nom_discussione, date_creation, id_bien=None):
        cur = self.db.cursor()
        cur.execute("INSERT INTO file_discussion (nom_discussione, date_creation, id_bien) VALUES (%s, %s, %s)", (nom_discussione, date_creation, id_bien))
        self.db.commit()
        cur.close()

    def delete_file_discussion(self, id_file_discussion):
        cur = self.db.cursor()
        cur.execute("DELETE FROM file_discussion WHERE id_file_discussion = %s", (id_file_discussion,))
        self.db.commit()
        cur.close()
    
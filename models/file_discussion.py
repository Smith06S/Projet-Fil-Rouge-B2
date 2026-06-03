class FileDiscussion:
    """Représente une agence (Entité)"""
    def __init__(self, id_file_discussion, nom_discussione, date_creation, id_bien=None, id_commercial=None, id_client=None):
        self.id_file_discussion = id_file_discussion
        self.nom_discussione = nom_discussione
        self.date_creation = date_creation
        self.id_bien = id_bien
        self.id_commercial = id_commercial
        self.id_client = id_client

class FileDiscussionRepository:
    """Gère la communication avec la table 'file discussion'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all(self, id_client=None, id_commercial=None):
        cur = self.db.cursor()
        if id_client is not None:
            cur.execute(
                "SELECT id_file_discussion, nom_discussione, date_creation, id_bien, id_commercial, id_client FROM file_discussion WHERE id_client = %s",
                (id_client,)
            )
        elif id_commercial is not None:
            cur.execute(
                "SELECT id_file_discussion, nom_discussione, date_creation, id_bien, id_commercial, id_client FROM file_discussion WHERE id_commercial = %s",
                (id_commercial,)
            )
        else:
            cur.close()
            return []

        rows = cur.fetchall()
        file_discussions = [FileDiscussion(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]

        cur.close()
        return file_discussions

    def find_existing_discussion(self, id_bien, id_commercial, id_client):
        """Trouve une discussion existante entre le même commercial et client pour le même bien"""
        cur = self.db.cursor()
        cur.execute(
            "SELECT id_file_discussion, nom_discussione, date_creation, id_bien, id_commercial, id_client FROM file_discussion WHERE id_bien = %s AND id_commercial = %s AND id_client = %s",
            (id_bien, id_commercial, id_client)
        )
        row = cur.fetchone()
        cur.close()
        if row:
            return FileDiscussion(row[0], row[1], row[2], row[3], row[4], row[5])
        return None

    def create_file_discussion(self, nom_discussione, date_creation, id_bien=None, id_commercial=None, id_client=None):
        cur = self.db.cursor()
        cur.execute(
            "INSERT INTO file_discussion (nom_discussione, date_creation, id_bien, id_commercial, id_client) VALUES (%s, %s, %s, %s, %s)",
            (nom_discussione, date_creation, id_bien, id_commercial, id_client)
        )
        self.db.commit()
        cur.close()

    def delete_file_discussion(self, id_file_discussion):
        cur = self.db.cursor()
        cur.execute("DELETE FROM file_discussion WHERE id_file_discussion = %s", (id_file_discussion,))
        self.db.commit()
        cur.close()
    
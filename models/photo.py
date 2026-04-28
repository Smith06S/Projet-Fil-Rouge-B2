class Photo:
    """Représente une photo (Entité)"""
    def __init__(self, id_photo, lien, id_bien, id_agence):
        self.id_photo = id_photo
        self.lien = lien
        self.id_bien = id_bien
        self.id_agence = id_agence

class PhotoRepository:
    """Gère la communication avec la table 'photo'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all(self, id_bien):
        cur = self.db.cursor()
        cur.execute("SELECT id_photo, lien, id_agence FROM photo WHERE id_bien = %s",(id_bien,))
        rows = cur.fetchall()

        photos = [Photo(r[0], r[1], r[2]) for r in rows]

        cur.close()
        return photos
    
    def agence_Photo(self, id_agence):
        cur = self.db.cursor()
        cur.execute("SELECT id_photo, lien FROM photo WHERE id_bien = %s",(id_agence,))
        rows = cur.fetchall()

        photos = [Photo(r[0], r[1]) for r in rows]

        cur.close()
        return photos
class Piece:
    """Représente une piece (Entité)"""
    def __init__(self, id_piece, etage, nom_piece, metre_carre_piece, id_bien):
        self.id_piece = id_piece
        self.etage = etage
        self.nom_piece = nom_piece
        self.metre_carre_piece = metre_carre_piece
        self.id_client = id_bien

class PieceRepository:
    """Gère la communication avec la table 'piece'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_by_bien(self, id_bien):
        cur = self.db.cursor()
        cur.execute("SELECT id_piece, etage, nom_piece, metre_carre_piece, id_bien FROM piece WHERE id_bien = %s", (id_bien,))
        rows = cur.fetchall()
        pieces = [Piece(r[0], r[1], r[2], r[3], r[4]) for r in rows]
        cur.close()
        return pieces
class Transaction:
    """Représente une transaction (Entité)"""
    def __init__(self, id_transaction, date_vente, prix_final, id_bien, id_commercial):
        self.id_transaction = id_transaction
        self.date_vente = date_vente
        self.prix_final = prix_final
        self.id_bien = id_bien
        self.id_commercial = id_commercial

class TransactionRepository:
    """Gère la communication avec la table 'transaction'"""
    def __init__(self, db_connexion):
        self.db = db_connexion

    def find_all(self):
        cur = self.db.cursor()
        cur.execute("SELECT id_transaction, date_vente, prix_final, id_bien, id_commercial FROM transaction")
        rows = cur.fetchall()

        transactions = [Transaction(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]

        cur.close()
        return transactions
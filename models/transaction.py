class TransactionRepository:
    def __init__(self, db_connection):
        self.db = db_connection

    def register_sale(self, prix_final, id_bien, id_client, id_commercial):
        with self.db.cursor() as cur:
            cur.execute("""
                INSERT INTO transaction (prix_final, id_bien, id_client, id_commercial)
                VALUES (%s, %s, %s, %s)
            """, (prix_final, id_bien, id_client, id_commercial))
            
            cur.execute("UPDATE bien SET statut = 'Vendu' WHERE id_bien = %s", (id_bien,))
        self.db.commit()
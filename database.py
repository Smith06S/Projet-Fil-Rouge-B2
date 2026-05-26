import psycopg2

class Database:
    def __init__(self):
        self.host = 'localhost'  # Cambia se necessario
        self.database = 'ymmodb'  # Nome del tuo database
        self.user = 'postgres'    # Cambia se necessario
        self.password = 'ymmo123'  # Cambia con la tua password

    def get_connection(self):
        return psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )

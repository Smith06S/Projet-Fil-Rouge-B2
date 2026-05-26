import psycopg2

class Database:
    def __init__(self):
        self.host = "localhost"
        self.database = "ymmodb"
        self.user = "postgres"
        self.password = "ymmo123"
        self.port = "5432"

    def get_connection(self):
        return psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port
        )

    def execute_query(self, query, params=None):
        """Exécute une requête de modification (INSERT, UPDATE, DELETE)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def fetch_all(self, query, params=None):
        """Récupère un ensemble de résultats (SELECT global)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def fetch_one(self, query, params=None):
        """Récupère un seul résultat (SELECT unique)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()
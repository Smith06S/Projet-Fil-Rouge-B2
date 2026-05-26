import psycopg2

class Database:
    def __init__(self):
        self.host = "localhost"
        self.database = "postgres"
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
        """Pour les requêtes de type INSERT, UPDATE, DELETE"""
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
        """Pour récupérer plusieurs lignes (SELECT)"""
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
        """Pour récupérer une seule ligne (SELECT ... LIMIT 1)"""
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
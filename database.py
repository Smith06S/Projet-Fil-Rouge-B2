import psycopg2

class Database:
    def get_connection(self):
        return psycopg2.connect(
            host="localhost",
            database="ymmodb",
            user="postgres",
            password="ymmo123"
        )

import psycopg2

class Database:
    def __init__(self):
        self.host = 'localhost'  
        self.database = 'ymmodb'  
        self.user = 'postgres'   
        self.password = 'ymmo123'

    def get_connection(self):
        return psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )

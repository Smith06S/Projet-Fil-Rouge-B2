import psycopg2
from psycopg2.extras import DictCursor

class Database:
    def __init__(self):
        self.config = {
            'dbname': 'ymmo',
            'user': 'postgres',
            'password': 'ymmo123',
            'host': 'localhost',
            'port': 5432
        }

    def get_connection(self):
        return psycopg2.connect(**self.config, cursor_factory=DictCursor)
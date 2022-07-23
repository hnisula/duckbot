import psycopg2

class PgStorage:
    def init(self, host, db_name, username, password):
        self.connection = psycopg2.connect(host=host, database=db_name, user=username, password=password)
        self.cursor = self.connection.cursor()
    
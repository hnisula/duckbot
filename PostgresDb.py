import psycopg2

class PostgresDb:
    @classmethod
    async def connect(cls, host, db_name, username, password):
        cls.connection = psycopg2.connect(host=host, database=db_name, user=username, password=password)
        cls.cursor = cls.connection.cursor()

        return cls

    def execute(self, query, params):
        self.cursor.execute(query, params)

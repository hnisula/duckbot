import json

class MatrixClientPgStorage:
    config = {
        "since": None
    }
    
    @classmethod
    def create(cls, pg_connection):
        instance = cls(pg_connection)

        instance.__ensure_table()
        instance.load()

        return instance
    
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def store(self):
        with self.pg_conn.cursor() as cursor:
            # TODO: Investigate a consistent way to insert and read jsonb with psycopg2
            # rather than using string in one place
            cursor.execute(
                '''
                    UPDATE matrix_client
                    SET json = %s
                    WHERE id='config'
                ''',
                (json.dumps(self.config),))
            self.pg_conn.commit()
    
    def load(self):
        with self.pg_conn.cursor() as cursor:
            cursor.execute("SELECT * FROM matrix_client WHERE id='config'")
            existing_config = cursor.fetchone()

            if existing_config:
                self.config = existing_config[1]

    def __ensure_table(self):
        with self.pg_conn.cursor() as cursor:
            cursor.execute('''
                    SELECT * FROM information_schema.tables
                    WHERE table_name='matrix_client'
                    LIMIT 1;
                ''')
            self.pg_conn.commit()
            matched_table = cursor.fetchone()
            
            if not matched_table:
                cursor.execute('''
                    CREATE TABLE matrix_client
                    (
                        id CHAR(64) PRIMARY KEY NOT NULL,
                        json JSONB NOT NULL
                    );

                    INSERT INTO matrix_client VALUES('config', '{}');
                ''')
                self.pg_conn.commit()
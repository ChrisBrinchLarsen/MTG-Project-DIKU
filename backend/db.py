import psycopg2
import psycopg2.extras

DB_HOST = "localhost"
DB_NAME = "dis_magic"
DB_USER = "admin"
DB_PASSWORD = "password"


class DB:
    conn = None
    cur = None

    @staticmethod
    def init():
        DB.conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD)

        DB.cur = DB.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    @staticmethod
    def execute(query: str, vars=None):
        DB.cur.execute(query, vars)
        return [dict(row) for row in DB.cur.fetchall()]

    @staticmethod
    def close():
        DB.conn.close()
        DB.cur.close()

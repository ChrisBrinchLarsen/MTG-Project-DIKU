import psycopg2

DB_HOST = "localhost"
DB_NAME = "dis_magic"
DB_USER = "admin"
DB_PASSWORD = "password"


def get_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD)

    return conn

import psycopg2
import db

conn = psycopg2.connect(
    host=db.DB_HOST,
    database=db.DB_NAME,
    user=db.DB_USER,
    password=db.DB_PASSWORD)

cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS cards;')
cur.execute('CREATE TABLE cards (id serial PRIMARY KEY,'
            'name varchar (150) NOT NULL,'
            'artist varchar (150) NOT NULL);'
            )

cur.execute('INSERT INTO cards (name, artist)'
            'VALUES (%s, %s)',
            ('Sample card 1', 'Sample artist 1')
            )

conn.commit()

cur.close()
conn.close()

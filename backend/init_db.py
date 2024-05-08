import psycopg2
import db
from backend.cardParser import parseCards

conn = psycopg2.connect(
    host=db.DB_HOST,
    database=db.DB_NAME,
    user=db.DB_USER,
    password=db.DB_PASSWORD)

cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Cards;')
cur.execute('CREATE TABLE cards (id serial PRIMARY KEY,'
            'name varchar (150) NOT NULL,'
            'releaseDate varchar (32) NOT NULL,'
            'cmc INT NOT NULL,'
            'oracle varchar (250) NOT NULL,'
            'collectorID varchar (8) NOT NULL,'
            'flavorText varchar (250) NOT NULL,'
            'priceEUR varchar (8) NOT NULL,'
            'imageSmall varchar (200) NOT NULL,'
            'imageNormal varchar (200) NOT NULL,'
            'imageLarge varchar (200) NOT NULL,'
            'setAcro varchar (8) NOT NULL,'
            'rarity varchar (16) NOT NULL,'
            'artist varchar (150) NOT NULL);'
            )

def insertCard(card):
    cur.execute('INSERT INTO Cards (name,'
                                   'releaseDate,'
                                   'cmc,'
                                   'oracle,'
                                   'collectorID,'
                                   'flavorText,'
                                   'priceEUR,'
                                   'imageSmall,'
                                   'imageNormal,'
                                   'imageLarge,'
                                   'setAcro,'
                                   'rarity,'
                                   'artist)'
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (card["name"]
                ,card["releaseDate"]
                ,card["combinedMana"]
                ,card["oracleText"]
                ,card["collectorID"]
                ,card["flavorText"]
                ,card["priceEUR"]
                ,card["imageSmall"]
                ,card["imageNormal"]
                ,card["imageLarge"]
                ,card["setAcro"]
                ,card["rarity"]
                ,card["artist"]
                )
        )


map(insertCard, parseCards("rawCards.json"))


#cur.execute('INSERT INTO Cards (name, artist)'
#            'VALUES (%s, %s)',
#            ('Sample card 1', 'Sample artist 1')
#            )

conn.commit()

cur.close()
conn.close()

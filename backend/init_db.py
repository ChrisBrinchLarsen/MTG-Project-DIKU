import psycopg2
import db
from card_parser import parse_cards

conn = psycopg2.connect(
    host=db.DB_HOST,
    database=db.DB_NAME,
    user=db.DB_USER,
    password=db.DB_PASSWORD)

cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Cards;')
cur.execute('CREATE TABLE Cards (cardID INTEGER PRIMARY KEY,'
            'name varchar (150)        NOT NULL,'
            'releaseDate date          NOT NULL,'
            'cmc INTEGER               NOT NULL,'
            'oracle varchar (950)      NOT NULL,'
            'collectorID varchar (10)  NOT NULL,'
            'flavorText varchar (450)  NOT NULL,'
            'priceEUR real             NOT NULL,'
            'imageSmall varchar (100)  NOT NULL,'
            'imageNormal varchar (100) NOT NULL,'
            'imageLarge varchar (100)  NOT NULL,'
            'setAcro varchar (8)       NOT NULL,'
            'rarity varchar (8)        NOT NULL,'
            'artist varchar (55)       NOT NULL);'
            )

# Color relation
cur.execute('DROP TABLE IF EXISTS ColorCards;')
cur.execute("""
CREATE TABLE ColorCards (
cardID INTEGER NOT NULL,
color varchar (1) DEFAULT 0,
PRIMARY KEY(cardID, color)
);
"""
            )

# Keyword relation
cur.execute('DROP TABLE IF EXISTS KeywordCards;')
cur.execute("""
CREATE TABLE KeywordCards (
cardID INTEGER NOT NULL,
keyword varchar (64),
PRIMARY KEY(cardID, keyword)
);
"""
            )

# Type relation
cur.execute('DROP TABLE IF EXISTS TypeCards;')
cur.execute("""
CREATE TABLE TypeCards (
cardID INTEGER NOT NULL,
type varchar (32),
PRIMARY KEY(cardID, type)
);
"""
            )

# Super type relation
cur.execute('DROP TABLE IF EXISTS SuperTypeCards;')
cur.execute("""
CREATE TABLE SuperTypeCards (
cardID INTEGER NOT NULL,
superType varchar (32),
PRIMARY KEY(cardID, superType)
);
"""
            )

# SUb type relation
cur.execute('DROP TABLE IF EXISTS SubTypeCards;')
cur.execute("""
CREATE TABLE SubTypeCards (
cardID INTEGER NOT NULL,
subType varchar (32),
PRIMARY KEY(cardID, subType)
);
"""
            )

# Card inserter


def insertCard(card, id):
    insertQuery = """
    INSERT INTO Cards (cardID, name, releaseDate, cmc, oracle, collectorID, flavorText, priceEUR, imageSmall, imageNormal, imageLarge, setAcro, rarity, artist) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cardInfo = (id, card["name"], card["releaseDate"], card["combinedMana"], card["oracleText"], card["collectorID"], card["flavorText"], card["priceEUR"], card["imageSmall"], card["imageNormal"], card["imageLarge"], card["setAcro"], card["rarity"], card["artist"]
                )
    cur.execute(insertQuery, cardInfo)

# Color-card inserter


def insertColorCard(card, id):
    insertQuery = """
    INSERT INTO ColorCards (cardID, color)
    VALUES (%s, %s)
    """
    for color in card["colors"]:
        cur.execute(insertQuery, (id, color))

# Keyword-card inserter


def insertKeywordCard(card, id):
    insertQuery = """
    INSERT INTO KeywordCards (cardID, keyword)
    VALUES (%s, %s)
    """
    for keyword in card["keywords"]:
        cur.execute(insertQuery, (id, keyword))

# Type-card inserter


def insertTypeCard(card, id):
    insertQuery = """
    INSERT INTO TypeCards (cardID, type)
    VALUES (%s, %s)
    """
    for type in card["types"]:
        cur.execute(insertQuery, (id, type))

# Supertype-card inserter


def insertSuperTypeCard(card, id):
    insertQuery = """
    INSERT INTO SuperTypeCards (cardID, superType)
    VALUES (%s, %s)
    """
    for superType in card["superTypes"]:
        cur.execute(insertQuery, (id, superType))

# Subtype-card inserter


def insertSubTypeCard(card, id):
    insertQuery = """
    INSERT INTO SubTypeCards (cardID, subType)
    VALUES (%s, %s)
    """
    for subType in card["subTypes"]:
        cur.execute(insertQuery, (id, subType))


# Parse all cards from the dataset
cards = parse_cards("rawCards.json")
print("Uploading cards to database...")
id = 0  # Manually tracking individual card ID's for cross referencing tables
for card in cards:
    id += 1
    insertCard(card, id)
    insertColorCard(card, id)
    insertKeywordCard(card, id)
    insertTypeCard(card, id)
    insertSuperTypeCard(card, id)
    insertSubTypeCard(card, id)

conn.commit()

cur.close()
conn.close()

print("Done!\n")

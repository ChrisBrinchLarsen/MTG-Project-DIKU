import json
from flask import Flask, request
from flask_cors import CORS
from db import DB

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])


@app.route('/init-game', methods=['GET'])
def init_game():
    DB.init()

    # Initialize a random card to be the correct card
    correct_card = DB.execute(
        "SELECT cardid, name, cmc, imagesmall, imagenormal FROM cards ORDER BY RANDOM() LIMIT 1")[0]
    correct_card_id = correct_card["cardid"]

    # Initialize additional random cards
    cards = DB.execute("SELECT cardid, name, cmc, imagesmall, imagenormal FROM cards WHERE NOT cardid = %s ORDER BY RANDOM() LIMIT 999",
                       (correct_card_id,))

    DB.close()

    response = {
        "correctCard": correct_card,
        "cards": cards
    }

    return json.dumps(response, default=str)


@app.route('/guess', methods=['POST'])
def guess_card():
    DB.init()

    body = request.get_json()
    correct_card_id = body["correctCardId"]
    guessed_card_id = body["guessedCardId"]
    card_ids = body["cardIds"]

    # Fetch the correct card from ID
    correct_cards = DB.execute(
        """SELECT * FROM cards 
        LEFT JOIN typecards ON cards.cardid = typecards.cardid
        LEFT JOIN keywordcards ON cards.cardid = keywordcards.cardid
        LEFT JOIN subtypecards ON cards.cardid = subtypecards.cardid
        LEFT JOIN supertypecards ON cards.cardid = supertypecards.cardid
        LEFT JOIN colorcards ON cards.cardid = colorcards.cardid
        WHERE cards.cardid = %s""", (correct_card_id,))
    correct_cards[0]["type"] = list(
        set([card["type"] for card in correct_cards]))
    correct_cards[0]["supertype"] = list(
        set([card["supertype"] for card in correct_cards]))
    correct_cards[0]["color"] = list(
        set([card["color"] for card in correct_cards]))
    correct_cards[0]["subtype"] = list(
        set([card["subtype"] for card in correct_cards]))
    correct_cards[0]["keyword"] = list(
        set([card["keyword"] for card in correct_cards]))
    correct_card = correct_cards[0]

    # Fetch the guessed card from ID
    guessed_cards = DB.execute(
        """SELECT * FROM cards
        LEFT JOIN typecards ON cards.cardid = typecards.cardid
        LEFT JOIN keywordcards ON cards.cardid = keywordcards.cardid
        LEFT JOIN subtypecards ON cards.cardid = subtypecards.cardid
        LEFT JOIN supertypecards ON cards.cardid = supertypecards.cardid
        LEFT JOIN colorcards ON cards.cardid = colorcards.cardid
        WHERE cards.cardid = %s""", (guessed_card_id,))
    guessed_cards[0]["type"] = list(
        set([card["type"] for card in guessed_cards]))
    guessed_cards[0]["supertype"] = list(
        set([card["supertype"] for card in guessed_cards]))
    guessed_cards[0]["color"] = list(
        set([card["color"] for card in guessed_cards]))
    guessed_cards[0]["subtype"] = list(
        set([card["subtype"] for card in guessed_cards]))
    guessed_cards[0]["keyword"] = list(
        set([card["keyword"] for card in guessed_cards]))
    guessed_card = guessed_cards[0]

    # Create the query and args for selecting the cards in the game with the shared traits
    query = """
        SELECT DISTINCT cards.cardid 
        FROM cards
        LEFT JOIN typecards ON cards.cardid = typecards.cardid
        LEFT JOIN keywordcards ON cards.cardid = keywordcards.cardid
        LEFT JOIN subtypecards ON cards.cardid = subtypecards.cardid
        LEFT JOIN supertypecards ON cards.cardid = supertypecards.cardid
        LEFT JOIN colorcards ON cards.cardid = colorcards.cardid
        WHERE cards.cardid = ANY(%s)
        """

    args = (card_ids,)

    # Initialize an object containing information about whether each trait was correctly guessed
    guess = {}

    TRAITS_TO_COMPARE_ONE_TO_ONE = ["name", "rarity", "cmc", "releasedate"]
    TRAITS_TO_COMPARE_ONE_TO_MANY = [
        "color", "supertype", "type", "subtype", "keyword"]

    # For each one-to-one trait, check if the trait was guessed correctly and add the filter to the query
    for trait in TRAITS_TO_COMPARE_ONE_TO_ONE:
        correct_value = correct_card[trait]
        guessed_value = guessed_card[trait]

        if correct_value == guessed_value:
            # Do positive filtering if they share the same trait
            query = query + f"AND {trait} = '{guessed_value}'"
            guess[trait] = {
                "correctValues": [guessed_value],
                "incorrectValues": []
            }
        else:
            # Do negative filtering if they don't share the same trait
            query = query + f"AND NOT {trait} = '{guessed_value}'"
            guess[trait] = {
                "correctValues": [],
                "incorrectValues": [guessed_value]
            }

    # For each one-to-many trait, check if the trait is contained in the correct traits and add appropriate filters
    for trait in TRAITS_TO_COMPARE_ONE_TO_MANY:
        # Find the trait values the cards share
        common_values = [elm for elm in guessed_card[trait]
                         if elm in correct_card[trait]]

        # Find the trait values the cards do not share
        non_common_values = [card for card in guessed_card[trait]
                             if card not in correct_card[trait]]
        
        # Check if the common values for this trait encompasses ALL values of this trait on the correct card. 
        partialOrNot = "correct" if len(common_values) == len(correct_card[trait]) else "partial"

        # Do positive filtering on common traits
        if len(common_values) > 0:
            if common_values[0] == None:
                query += f"AND {trait} IS NULL "
            else:
                query += f"AND {trait} = ANY(%s) "
                args = args + ((common_values,))

        # Do negative filtering on non-common traits
        if len(non_common_values) > 0:
            if non_common_values[0] == None:
                query += f"AND {trait} IS NOT NULL "
            else:
                trait_table_name = f"{trait}cards"

                query += f"""AND cards.cardid NOT IN 
                    (SELECT cards.cardid FROM cards 
                    LEFT JOIN {trait_table_name} ON cards.cardid = {trait_table_name}.cardid 
                    WHERE {trait} = ANY(%s))
                    """

                args = args + ((non_common_values,))

        guess[trait] = {
            "correctValues": common_values,
            "incorrectValues": non_common_values,
            "status": partialOrNot
        }

    # Use a query that removes duplicates from the original query
    no_duplicate_query = f"SELECT cardid, name, imagesmall, imagenormal FROM ({query}) AS distinct_cards NATURAL JOIN cards"

    # Select the filtered cards
    filtered_cards = DB.execute(no_duplicate_query, args)

    DB.close()

    response = {
        "cards": filtered_cards,
        "guess": guess
    }

    return json.dumps(response, default=str)


@app.route('/get-card', methods=['POST'])
def get_card():
    DB.init()

    body = request.get_json()
    card_id = body["cardId"]

    cards = DB.execute("SELECT * FROM cards WHERE cardid = %s", (card_id,))

    DB.close()

    return json.dumps(cards[0], default=str)


if __name__ == '__main__':
    app.run(port=5000)

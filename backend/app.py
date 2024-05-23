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
        "SELECT cardid, name, cmc, imagesmall FROM cards ORDER BY RANDOM() LIMIT 1")[0]
    correct_card_id = correct_card["cardid"]

    # Initialize additional random cards
    cards = DB.execute("SELECT cardid, name, cmc, imagesmall FROM cards WHERE NOT cardid = %s ORDER BY RANDOM() LIMIT 19",
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
        "SELECT * FROM cards NATURAL JOIN typecards WHERE cardid = %s", (correct_card_id,))
    correct_cards[0]["type"] = [card["type"] for card in correct_cards]
    correct_card = correct_cards[0]

    # Fetch the guessed card from ID
    guessed_cards = DB.execute(
        "SELECT * FROM cards NATURAL JOIN typecards WHERE cardid = %s", (guessed_card_id,))
    guessed_cards[0]["type"] = [card["type"] for card in guessed_cards]
    guessed_card = guessed_cards[0]

    # Create the query and args for selecting the cards in the game with the shared traits
    query = """
        SELECT DISTINCT cardid 
        FROM cards 
        NATURAL JOIN typecards 
        WHERE cardid = ANY(%s) 
        """
    args = (card_ids,)

    # Initialize an object containing information about whether each trait was correctly guessed
    guess = {}

    TRAITS_TO_COMPARE_ONE_TO_ONE = ["rarity", "cmc"]
    TRAITS_TO_COMPARE_ONE_TO_MANY = ["type"]

    # For each one-to-one trait, check if the trait was guessed correctly and add the filter to the query
    for trait in TRAITS_TO_COMPARE_ONE_TO_ONE:
        correct_value = correct_card[trait]
        guessed_value = guessed_card[trait]

        if correct_value == guessed_value:
            query = query + f"AND {trait} = '{guessed_value}'"
            guess[trait] = {
                "correctValues": [guessed_value],
                "incorrectValues": []
            }
        else:
            query = query + f"AND NOT {trait} = '{guessed_value}'"
            guess[trait] = {
                "correctValues": [],
                "incorrectValues": [guessed_value]
            }

    # For each one-to-many trait, check if the trait is contained in the correct traits and add appropriate filters
    for trait in TRAITS_TO_COMPARE_ONE_TO_MANY:
        # Find the trait values the cards share
        common_values = [card for card in guessed_card[trait]
                         if card in correct_card[trait]]

        # Find the trait values the cards do not share
        non_common_values = [card for card in guessed_card[trait]
                             if card not in correct_card[trait]]

        if len(common_values) > 0:
            query = query + f"AND {trait} = ANY(%s)"
            args = args + ((common_values,)
                           if len(common_values) > 0 else ())

        if len(non_common_values) > 0:
            query = query + f"AND NOT {trait} = ANY(%s)"
            args = args + ((non_common_values,)
                           if len(non_common_values) > 0 else ())

        guess[trait] = {
            "correctValues": common_values,
            "incorrectValues": non_common_values
        }

    # Use a query that removes duplicates from the original query
    no_duplicate_query = f"SELECT cardid, name, imagesmall FROM ({query}) AS distinct_cards NATURAL JOIN cards"

    # Select the filtered cards
    filtered_cards = DB.execute(no_duplicate_query, args)

    DB.close()

    response = {
        "cards": filtered_cards,
        "guess": guess
    }

    return json.dumps(response, default=str)


if __name__ == '__main__':
    app.run(port=5000)

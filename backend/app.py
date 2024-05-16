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
        "SELECT cardid, name, imagesmall FROM cards ORDER BY RANDOM() LIMIT 1")[0]
    correct_card_id = correct_card["cardid"]

    # Initialize additional random cards
    cards = DB.execute("SELECT cardid, name, imagesmall FROM cards WHERE NOT cardid = %s ORDER BY RANDOM() LIMIT 19",
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
    correct_card = DB.execute(
        "SELECT * FROM cards WHERE cardid = %s", (correct_card_id,))[0]

    # Fetch the guessed card from ID
    guessed_card = DB.execute(
        "SELECT * FROM cards WHERE cardid = %s", (guessed_card_id,))[0]

    CATEGORIES_TO_COMPARE = ["rarity"]

    # Find the traits that the guessed and correct card share
    matching_traits = {key: value for (key, value) in
                       guessed_card.items() if correct_card[key] == value and key in CATEGORIES_TO_COMPARE}

    # Find the traits that the guessed and correct card do not share
    non_matching_traits = {key: value for (key, value) in
                           guessed_card.items() if correct_card[key] != value and key in CATEGORIES_TO_COMPARE}

    # Create the query for selecting the cards in the game with the shared traits
    base_query = "SELECT cardid, name, imagesmall FROM cards WHERE cardid = ANY(%s) "

    # Create the SQL conditionals for matching traits (positive filters)
    positive_filter_conds = [f"AND {trait} = '{value}'" for trait,
                             value in matching_traits.items()]
    # Create the SQL conditionals for traits that do not match (negative filters)
    negative_filter_conds = [f"AND NOT {trait} = '{value}'" for trait,
                             value in non_matching_traits.items()]

    # Concatenate the conditionals with the base query
    query = base_query + \
        ' '.join(positive_filter_conds) + ' '.join(negative_filter_conds)

    # Select the filtered cards
    filtered_cards = DB.execute(query, (card_ids,))

    DB.close()

    response = {
        "cards": filtered_cards
    }

    return json.dumps(response, default=str)


if __name__ == '__main__':
    app.run(port=5000)

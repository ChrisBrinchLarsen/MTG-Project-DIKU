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

    CATEGORIES_TO_COMPARE = ["rarity", "cmc"]

    # Find the traits that the guessed and correct card share
    matching_traits = {key: value for (key, value) in
                       guessed_card.items() if correct_card[key] == value and key in CATEGORIES_TO_COMPARE}

    # Find the traits that the guessed and correct card do not share
    non_matching_traits = {key: value for (key, value) in
                           guessed_card.items() if correct_card[key] != value and key in CATEGORIES_TO_COMPARE}

    # Create the query for selecting the cards in the game with the shared traits
    base_query = """
        SELECT DISTINCT cardid 
        FROM cards 
        NATURAL JOIN typecards 
        WHERE cardid = ANY(%s) 
        """

    # Create the SQL conditionals for matching traits (positive filters)
    positive_filter_conds = [f"AND {trait} = '{value}'" for trait,
                             value in matching_traits.items()]
    # Create the SQL conditionals for traits that do not match (negative filters)
    negative_filter_conds = [f"AND NOT {trait} = '{value}'" for trait,
                             value in non_matching_traits.items()]

    # Find the types the card shares
    common_types = [card for card in correct_card["type"]
                    if card in guessed_card["type"]]

    # Calculate the SQL conditional for matching types
    positive_filters_type = "AND type = ANY(%s)" if len(
        common_types) > 0 else ""

    # Concatenate the conditionals with the base query
    query = base_query + \
        ' '.join(positive_filter_conds) + \
        ' '.join(negative_filter_conds) + positive_filters_type

    # Construct the args
    common_types_tuple = (common_types,) if len(common_types) > 0 else ()
    args = (card_ids, *common_types_tuple)

    # Use a query that removes duplicates from the original query
    no_duplicate_query = f"SELECT cardid, name, imagesmall FROM ({query}) AS distinct_cards NATURAL JOIN cards"

    # Select the filtered cards
    filtered_cards = DB.execute(no_duplicate_query, args)

    DB.close()

    response = {
        "cards": filtered_cards
    }

    return json.dumps(response, default=str)


if __name__ == '__main__':
    app.run(port=5000)

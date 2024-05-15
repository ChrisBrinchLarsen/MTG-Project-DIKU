import psycopg2.extras
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_db

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])


@app.route('/random-cards', methods=['GET'])
def get_cards():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM cards ORDER BY RANDOM() LIMIT 20")
    cards = cur.fetchall()

    cur.close()
    conn.close()

    return json.dumps(cards, default=str)

@app.route('/guess', methods=['POST'])
def guess_card(): 
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    print(request.get_json())

    cur.close()
    conn.close()
    return "success"

if __name__ == '__main__':
    app.run(port=5000)

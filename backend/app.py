from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

employees = [{'id': 1, 'name': 'Ashley'}, {
    'id': 2, 'name': 'Kate'}, {'id': 3, 'name': 'Joe'}]


@app.route('/employees', methods=['GET'])
# in its current form, the /employees route returns JSON containing sample data
def get_employees():
    return jsonify(employees)


if __name__ == '__main__':
    app.run(port=5000)

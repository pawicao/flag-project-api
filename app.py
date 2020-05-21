import flask, json
from flask_cors import CORS
from flask import jsonify, request
from question_handler import get_response, questions

app = flask.Flask(__name__)
CORS(app)

# Get all countries
@app.route('/getAll', methods=['GET'])
def get_all_countries():
    with open('assets/all_countries.json', 'r') as file:
        response = flask.make_response(file.read(), 200)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.mimetype = "application/json"
        return response


# Get all countries and the first question
@app.route('/', methods=['GET'])
@app.route('/start', methods=['GET'])
def start():
    with open('assets/all_countries.json', 'r') as file:
        countries = file.read()
    response_content = '{ "countries": ' + countries + ',' + '"question":' + json.dumps({
        "id": 2,
        "content": questions[2]
    }) + '}'
    response = flask.make_response(response_content, 200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.mimetype = "application/json"
    return response


# Process answer, return filtered list of countries together with a new question
@app.route('/processQuestion', methods=['POST'])
def process_question():
    data = request.get_json()
    response = jsonify(get_response(data['countries'], data['question']['id'], data['answer']))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.mimetype = "application/json"
    return response


# Start the application
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

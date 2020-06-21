import flask, json
from flask_cors import CORS
from flask import jsonify, request

from img_analyzer.main_analyzer import new_first_shade_question
from utils.question_handler import get_response

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
    question_details = new_first_shade_question(json.loads(countries))
    dic_response = {
        "countries": json.loads(countries),
        "faulty_countries": question_details[2],
        "truthy_countries": question_details[1],
        "question": {
            "id": 554,
            "content": question_details[0]
        }
    }
    response = jsonify(dic_response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.mimetype = "application/json"
    return response


# Process answer, return filtered list of countries together with a new question
@app.route('/processQuestion', methods=['POST'])
def process_question():
    data = request.get_json()
    response = jsonify(get_response(data['truthy_countries'], data['faulty_countries'], data['answer']))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.mimetype = "application/json"
    return response


# Start the application
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

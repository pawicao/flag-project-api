import flask
from flask import request, jsonify

app = flask.Flask(__name__)

@app.route('/')
def home():
	response = jsonify("HOME PAGE!")
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response


# A route to return an example "Hello!"
@app.route('/hello', methods=['GET'])
def api_hello():
	response = jsonify("Elo, byku!")
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
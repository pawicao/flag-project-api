import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
@app.route('/home')
def home():
	response = jsonify("HOME PAGE!")
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response


# A route to return an example "Hello!"
@app.route('/hello', methods=['GET'])
def api_hello():
	response = jsonify("Elo!")
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

app.run()
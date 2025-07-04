from flask import Flask, jsonify, request
from tools import *

app = Flask(__name__)

@app.route('/check', methods=['GET'])
def check():
    return jsonify(message="Hey!,Im Nexa im Online")

@app.route('/web_search')
def greet():
    return jsonify(message="Today is sunday")

@app.route('/weather')
def weather():
    return get_weather()

@app.route('/')
def home():
    return jsonify(message="Hello")

if __name__ == '__main__':
    app.run(debug=True)
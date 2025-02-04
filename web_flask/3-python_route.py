#!/usr/bin/python3
""" Write a script that starts a Flask web application:
Your web application must be listening on 0.0.0.0, port 5000
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """returns a string"""
    return ("Hello HBNB!")


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """returns a string"""
    return ("HBNB")


@app.route('/c/<text>', strict_slashes=False)
def c_with_text(text):
    """display “C ”, followed by the value of the text variable"""
    return "C {}".format(text.replace("_", " "))


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_with_text(text):
    """display “Python ”, followed by the value of the text variable"""
    return "Python {}".format(text.replace("_", " "))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

#!/usr/bin/python3
"""
    This module starts a Flask web application run on
    a global server in port 5000
"""
from flask import Flask
from markupsafe import escape
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """
        Display a content when user navigate to the home page
    """
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """
        Display a content when user navigate to hbnb
    """
    return 'HBNB'


@app.route('/c/<text>')
def c_text(text):
    """
        Display a content when user navigate to c followed by
        the value of the text variable
    """
    txt = escape(text).replace('_', ' ')
    return f'C {txt}'


@app.route('/python')
@app.route('/python/<text>')
def python_text(text="is cool"):

    """ Display a content when user navigate to python followed by
        the value of the text variable.

    Returns:
        string: Python concatenate with a text pass as an argument
    """
    txt = escape(text).replace('_', ' ')
    return f'Python {txt}'


@app.route('/number/<int:n>')
def number_n(n):

    """ Display a content when user navigate to number followed by
        the value of the n variable.

    Returns:
        string: a number pass as an argument concate with 'is a number'
    """
    return f'{escape(n)} is a number'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

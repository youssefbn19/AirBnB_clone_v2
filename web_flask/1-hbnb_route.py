#!/usr/bin/python3
"""
    This module starts a Flask web application run on
    a global server in port 5000
"""
from flask import Flask
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

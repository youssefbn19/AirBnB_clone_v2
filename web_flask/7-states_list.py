#!/usr/bin/python3
"""
    This module starts a Flask web application run on
    a global server in port 5000
"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def tearDown_content(exception):
    """Remove the current data"""
    storage.close()


@app.route('/states_list')
def states_list():
    """Display a HTML page contains content about states"""
    states = storage.all('State').values()
    states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

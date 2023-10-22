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


@app.route('/states')
@app.route('/states/<id>')
def states_id(id=None):
    """Display a HTML page contains content about states and cities"""
    states = storage.all('State').values()
    cities = storage.all('City').values()
    states = sorted(states, key=lambda state: state.name)
    cities = sorted(cities, key=lambda city: city.name)
    if id is not None:
        if id in [state.id for state in states]:
            states = [state for state in states if state.id == id]
            cities = [city for city in cities if city.state_id == id]
        else:
            states = []
            cities = []
    return render_template('9-states.html',
                           states=states, cities=cities, id=id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

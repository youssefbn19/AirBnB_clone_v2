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


@app.route('/hbnb_filters')
def states_id():
    """Display a HTML page contains content about states and cities"""
    states = storage.all('State').values()
    cities = storage.all('City').values()
    amenities = storage.all('Amenity').values()
    states = sorted(states, key=lambda state: state.name)
    states = [state for state in states
              if state.id in [city.state_id for city in cities]]
    cities = sorted(cities, key=lambda city: city.name)
    amenities = sorted(amenities, key=lambda amenity: amenity.name)
    return render_template('10-hbnb_filters.html',
                           states=states, cities=cities, amenities=amenities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

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


@app.route('/hbnb')
def hbnb():
    """Display a HTML page contains in path hbnb"""
    states = storage.all('State').values()
    cities = storage.all('City').values()
    amenities = storage.all('Amenity').values()
    places = storage.all('Place').values()
    users = storage.all('User').values()
    for place in places:
        for user in users:
            if place.user_id == user.id:
                place.user_fname = f'{user.first_name} {user.last_name}'
                break
    states = sorted(states, key=lambda state: state.name)
    states = [state for state in states
              if state.id in [city.state_id for city in cities]]
    cities = sorted(cities, key=lambda city: city.name)
    amenities = sorted(amenities, key=lambda amenity: amenity.name)
    places = sorted(places, key=lambda place: place.name)
    return render_template('100-hbnb.html',
                           states=states, cities=cities,
                           amenities=amenities, places=places,)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

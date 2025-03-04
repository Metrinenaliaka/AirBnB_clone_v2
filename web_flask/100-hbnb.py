#!/usr/bin/python3
'''crates a flask web application'''
from flask import Flask, render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states')
@app.route('/states_list')
def display_states():
    return render_template('7-states_list.html', storage=storage.all('State'))


@app.route('/states/<id>')
def display_by_id(id):
    state_obj = None
    for obj in storage.all("State").values():
        if obj.id == id:
            state_obj = obj
    return render_template('9-states.html', storage=storage.all('State'),
                           state_obj=state_obj)


@app.route('/hbnb_filters')
def display_filters():
    return render_template('10-hbnb_filters.html',
                           storage=storage.all('State'),
                           amenity=storage.all('Amenity'))


@app.route('/hbnb')
def display_hbnb():
    return render_template('100-hbnb.html',
                           storage=storage.all('State'),
                           amenity=storage.all('Amenity'),
                           place=storage.all('Place'),
                           user=storage.all('User'))


@app.teardown_appcontext
def close(exception):
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')

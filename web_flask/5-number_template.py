#!/usr/bin/python3
'''crates a flask web application'''

from flask import Flask
from flask import render_template

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """routing home"""
    return ('Hello HBNB!')


@app.route('/hbnb')
def hbnb():
    """routing with path"""
    return ('HBNB')


@app.route('/c/<text>')
def c_is_fun(text):
    """rendering string"""
    return ('C %s' % text.replace("_", " "))


@app.route('/python', defaults={'text': 'is cool'})
@app.route('/python/<text>')
def python_is_cool(text):
    """rendering string with template"""
    return ('Python %s' % text.replace("_", " "))


@app.route('/number/<int:n>')
def num(n):
    """rendering int w/o template"""
    return ('%d is a number' % n)


@app.route('/number_template/<int:n>')
def num_tem(n):
    """rendering int with template"""
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

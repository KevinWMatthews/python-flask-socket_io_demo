from flask import render_template, Blueprint, abort
from jinja2 import TemplateNotFound
from socket_io_demo import app, socketio

default_view = Blueprint('index', __name__)

@app.route('/', defaults = {'page': 'index'})
@app.route('/<page>')
def show(page):
    try:
        return render_template('%s.html' % page)
    except TemplateNotFound:
        abort(404)

@socketio.on('connect')
def handle_connect():
    print 'connected'

@socketio.on('my event')
def handle_json(json):
    print 'received my event: ' + str(json)

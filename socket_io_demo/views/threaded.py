from flask import render_template, Blueprint, abort
from flask_socketio import emit, send
from jinja2 import TemplateNotFound
from socket_io_demo import app, socketio

threaded_view = Blueprint('threaded', __name__)

@app.route('/threaded')
def show_threaded():
    try:
        return render_template('threaded.html')
    except TemplateNotFound:
        abort(404)

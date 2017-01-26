from flask import render_template, Blueprint, abort
from flask_socketio import emit, send
from jinja2 import TemplateNotFound
from socket_io_demo import app, socketio
import json

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
    print 'Python SocketIO connected.'

@socketio.on('message')
def handle_message(message):
    print 'Python SocketIO received a message: "%s"' % message

@socketio.on('javascript_emit')
def handle_message(data):   # The python and javascript must agree on the message content
    print 'Python SocketIO received a javascript_emit: "%s"' % data

@socketio.on('custom event')
def handle_custom_event(message):
    print 'SocketIO - custom event: ' + message

@socketio.on('javascript_json')
def handle_json(json):  # flask-socketio is smart; it receives its message as a dict?
    print 'Python SocketIO received json: ' + str(json)
    print 'data: ' + json["data"]

@socketio.on('javascript_request_emit_custom_event')
def handle_custom_event(message):
    print 'Python SocketIO received a request to emit a custom event'
    message = 'Python SocketIO emitted a custom event'
    print message
    emit('custom event', message)

@socketio.on('javascript_request_send')
def handle_send_message(message):
    print 'Python SocketIO received a request to send a message'
    message = 'Python SocketIO sent a message'
    print message
    send(message)

# The Python emits the event and the javascript does nothing.
@socketio.on('javascript_request_unhandled')
def handle_emit_unhandled_event(message):
    print 'Python SocketIO received a request to emit an unhandled event'
    message = 'Python SocketIO emitted an event type that Javascript does not know about'
    print message
    emit('javascript_does_not_handle', message)

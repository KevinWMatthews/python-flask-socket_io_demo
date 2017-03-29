from flask import render_template, Blueprint, abort
from flask_socketio import emit, send
from jinja2 import TemplateNotFound
from socket_io_demo import app, socketio
import time
import eventlet
eventlet.monkey_patch()

threaded_view = Blueprint('threaded', __name__)

def a_thread():
    time.sleep(2)   # If you enter the thread too soon, the page won't have rendered yet
    send_message('You have entered the thread')
    while True:
        time.sleep(2)
        send_message('You have slept')
    send_message('You are leaving the thread')
    return

def thread_with_args(msg):
    time.sleep(2)
    send_message('You have entered the thread with arguments')
    while True:
        time.sleep(2)
        send_message(msg)

@app.route('/threaded')
def show_threaded():
    eventlet.spawn(a_thread)
    eventlet.spawn(thread_with_args, 'This is the argumentative thread')

    try:
        return render_template('threaded.html')
    except TemplateNotFound:
        abort(404)

def send_message(msg):
    print msg
    socketio.emit('message', msg)

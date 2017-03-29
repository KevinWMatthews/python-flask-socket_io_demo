from flask import render_template, Blueprint, abort
from flask_socketio import emit, send
from jinja2 import TemplateNotFound
from socket_io_demo import app, socketio
from threading import Thread
import time
import eventlet
# Event if you are spawning a thread using Thread, you must monkey patch python to emit from a background thread
eventlet.monkey_patch()

threaded_view = Blueprint('threaded', __name__)

def background_thread():
    time.sleep(2)
    send_message('Entering background thread')
    while True:
        time.sleep(1)
        send_message('Background thread woke up')

@app.route('/threaded')
def show_threaded():
    # Alternatively, you may use eventlet.spawn(background_thread)
    thread = Thread(target=background_thread)
    thread.daemon = True
    thread.start()

    try:
        return render_template('threaded.html')
    except TemplateNotFound:
        abort(404)

def send_message(msg):
    print msg
    socketio.emit('message', msg)

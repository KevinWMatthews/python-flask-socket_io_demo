from flask import render_template, Blueprint, abort, request
from werkzeug import secure_filename
import os
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

@app.route('/threaded', methods=['GET', 'POST'])
def show_threaded():
    if request.method == 'POST':
        print ''
        print 'Entering post'
        print request
        print request.files

        if 'uploaded_file' not in request.files:
            print 'could not find file'
            return 'could not find file'

        print 'getting file'
        file = request.files['uploaded_file']
        print 'got file'
        if file.filename == '':
            print 'File has no filename'
            return 'File has no filename'

        if file: #and allowed_filename(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('/tmp', filename))
            return 'OK'

        return 'error'

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

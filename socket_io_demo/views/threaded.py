from flask import render_template, Blueprint, abort, request, jsonify
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
            status_message = 'fail'
            error_message = 'Requested file not found'
            print error_message
            return jsonify(status_message = status_message, error_message = error_message)

        print 'getting file'
        file = request.files['uploaded_file']
        if not file:
            status_message = 'fail'
            error_message = 'Uploaded file not found'
            print error_message
            return jsonify(status_message = status_message, error_message = error_message)

        print 'got file'
        if file.filename == '':
            status_message = 'fail'
            error_message = 'Filename not found'
            print error_message
            return jsonify(status_message = status_message, error_message = error_message)

        # if not allowed_filename(file.filename):
            # status_message = 'fail'
            # error_message = 'Filetype not allowed'
            # print error_message
            # return jsonify(status_message = status_message, error_message = error_message)

        filename = secure_filename(file.filename)
        filepath = os.path.join('/tmp', filename)
        file.save(filepath)

        status_message = 'success'
        return jsonify(status_message = status_message)

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

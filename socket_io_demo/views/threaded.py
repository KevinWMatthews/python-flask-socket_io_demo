from flask import render_template, Blueprint, abort, request
from werkzeug import secure_filename
import os
from jinja2 import TemplateNotFound
from socket_io_demo import app

threaded_view = Blueprint('threaded', __name__)

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
            print file.read()
            return 'OK'

        return 'error'

    try:
        return render_template('threaded.html')
    except TemplateNotFound:
        abort(404)

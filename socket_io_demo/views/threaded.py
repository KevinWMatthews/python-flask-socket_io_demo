from flask import render_template, Blueprint, abort, request
from werkzeug import secure_filename
from jinja2 import TemplateNotFound
from socket_io_demo import app

import os
import tempfile

import flask
import werkzeug

# from saveserver import current_milli_time, intWithCommas, measure_spent_time

threaded_view = Blueprint('threaded', __name__)

@app.route('/threaded', methods=['GET', 'POST'])
def show_threaded():
    if request.method == 'POST':
        print 'New POST request'

        def custom_stream_factory(total_content_length, filename, content_type, content_length=None):
            tmpfile = tempfile.NamedTemporaryFile('wb+', prefix='flaskapp')
            print "start receiving file ... filename => " + str(tmpfile.name)
            return tmpfile

        # ms = measure_spent_time()

        stream,form,files = werkzeug.formparser.parse_form_data(flask.request.environ, stream_factory=custom_stream_factory)
        total_size = 0

        for fil in files.values():
            print " ".join(["saved form name", fil.name, "submitted as", fil.filename, "to temporary file", fil.stream.name])
            total_size += os.path.getsize(fil.stream.name)

    try:
        return render_template('threaded.html')
    except TemplateNotFound:
        abort(404)

from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('SOCKET_IO_DEMO_SETTINGS', silent = True)
socketio = SocketIO(app)

from views.default import default_view
from views.threaded import threaded_view

app.register_blueprint(default_view)
app.register_blueprint(threaded_view)

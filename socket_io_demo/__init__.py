from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('SOCKET_IO_DEMO_SETTINGS', silent = True)

from views.default import default_view

app.register_blueprint(default_view)

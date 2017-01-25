from socket_io_demo import app, socketio
import socket_io_demo.views
socketio.run(app, host='127.0.0.1', port=5000)

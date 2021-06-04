from flask import Flask
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
sio = SocketIO(app)

# Handle Input and Set State
@sio.on('move')
def handle_movement(sid, data):
  pass

@sio.on('press')
def handle_press(sid, data):
  pass

@sio.on('release')
def handle_release(sid, data):
  pass

# Run application
sio.run(app)

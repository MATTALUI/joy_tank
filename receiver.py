from flask import Flask
from flask_socketio import SocketIO
import logging
from Tank import Tank

# Initialize tanks state and connection
app = Flask(__name__)
sio = SocketIO(app)
tank = Tank()
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Root routing for connection testing
@app.route('/')
def index():
  return 'Hello, World!'

# Handle Input and Set State
@sio.on('move')
def handle_movement(data):
  tank.handle_movement(data)

@sio.on('press')
def handle_press(data):
  tank.handle_press(data)

@sio.on('release')
def handle_release(data):
  tank.handle_release(data)

@sio.event
def connect():
  print("========== Connection has been made successfully. ==========")

# Run application
sio.run(app, host='0.0.0.0', port='6969')

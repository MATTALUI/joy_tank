import pygame
import socketio
import math

# Initialize pygame for joystick readings
pygame.init()
if pygame.joystick.get_count() == 0:
  raise Exception("There is no controller available")
joystick = pygame.joystick.Joystick(0)
joystick.init()
axes = joystick.get_numaxes()

# Initialize socket connection to Tank
sio = socketio.Client()
sio.connect('http://0.0.0.0:6969')

axis_name_map = {
  "0": "X",
  "1": "Y",
  "2": "Z",
  "3": "THROTTLE",
}

state = {
  "0": f"{axis_name_map['0']} OFF +",
  "1": f"{axis_name_map['1']} OFF +",
  "2": f"{axis_name_map['2']} OFF +",
  "3": f"{axis_name_map['3']} OFF +",
}

def determine_power(value):
  normalized_value = abs(value * 100)
  if normalized_value > 66:
    return "HIGH"
  elif normalized_value > 33:
    return "LOW"
  return "OFF"

def determine_sign(axis, value):
  axis = str(axis)
  offset = 33
  # Making sure that the acis has passed an offset threshold helps to reduce state change
  # noise that occurs when changing from negative or positive numbers with low ABS value.
  if abs(value * 100) <= offset:
    return state[axis].split(' ')[2]
  if value > 0:
    return "+"
  else:
    return "-"

def convert_throttle_value(value):
  return math.floor((value*-50)+50)

def compare_axis_motion(axis, value):
  axis = str(axis)
  axis_name = axis_name_map[axis]
  power = determine_power(value)
  sign = determine_sign(axis, value)
  new_state = f"{axis_name} {power} {sign}"
  old_state = state[axis]
  is_throttle = axis_name == "THROTTLE"
  if is_throttle:
    value = convert_throttle_value(value)
  if is_throttle or new_state != old_state:
    state[axis] = new_state
    sio.emit('move', {
      "power": power,
      "axis": axis_name,
      "direction": sign,
      "value": value,
    })

while True:
  for event in pygame.event.get():
    if event.type == pygame.JOYBUTTONDOWN:
      sio.emit('press', event.button)
    elif event.type == pygame.JOYBUTTONUP:
      sio.emit('release', event.button)
    elif event.type == pygame.JOYAXISMOTION:
      compare_axis_motion(event.axis, event.value)

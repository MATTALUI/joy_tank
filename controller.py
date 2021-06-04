import pygame
import socketio

# Initialize pygame for joystick readings
pygame.init()
if pygame.joystick.get_count() == 0:
  raise Exception("There is no controller available")
joystick = pygame.joystick.Joystick(0)
joystick.init()
axes = joystick.get_numaxes()

# Initialize socket connection to Tank
sio = socketio.Client()
# sio.connect('http://localhost:5000')

axis_name_map = {
  "0": "X",
  "1": "Y",
  "2": "Z",
  "3": "THROTTLE",
}

# axis_dir_map = {
#   "0": "RIGHT",
#   "1": "BACK",
#   "2": "ROTATION CW",
#   "3": "THROTTLE DOWN",
# }

# neg_axis_dir_map = {
#   "0": "LEFT",
#   "1": "FORWARD",
#   "2": "ROTATION CCW",
#   "3": "THROTTLE UP",
# }

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
  if abs(value * 100) <= offset:
    return state[axis].split(' ')[2]
  if value > 0:
    return "+"
  else:
    return "-"

# def map_axis_motion(axis, value):
#   map = axis_dir_map
#   if value < 0:
#     map = neg_axis_dir_map
#   direction = map[axis]
#   power = determine_power(value)
#   print(f"{direction}: {power}")

def compare_axis_motion(axis, value):
  axis = str(axis)
  axis_name = axis_name_map[axis]
  power = determine_power(value)
  sign = determine_sign(axis, value)
  new_state = f"{axis_name} {power} {sign}"
  old_state = state[axis]
  if new_state != old_state:
    state[axis] = new_state
    print(new_state)

while True:
  for event in pygame.event.get():
    if event.type == pygame.JOYBUTTONDOWN:
      print(f"Joystick button pressed. {event.button}")
    elif event.type == pygame.JOYBUTTONUP:
      print(f"Joystick button released. {event.button}")
    elif event.type == pygame.JOYAXISMOTION:
      compare_axis_motion(event.axis, event.value)

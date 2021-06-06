from enum import Enum
from threading import Thread
from time import sleep
# from gpiozero import Led, Servo

class Tank:
  class Pins(Enum):
    WHEEL_RIGHT=None
    WHEEL_LEFT=None
    LED_TURRET=None
    LED_DRIVE=None
    LED_HEAD=None

  def __init__(self):
    self.is_firing = False
    # self.turret_led = Led(self.Pins.LED_TURRET)
    # self.head_led = Led(self.Pins.LED_HEAD)
    # self.drive_led = Led(self.Pins.LED_DRIVE)
    # self.left_wheel = Servo(self.Pins.WHEEL_LEFT)
    # self.left_right = Servo(self.Pins.WHEEL_RIGHT)
    # self.update_thread = self._initialize_update_thread()

  def handle_movement(self, data):
    axis = data['axis']
    handler = {
      "X": lambda: self._handle_turning(data),
      "Y": lambda: self._handle_acceleration(data),
      "Z": lambda: self._handle_turret_rotation(data),
      "THROTTLE": lambda: self._handle_throttle(data),
    }.get(str(axis)) or (lambda: None)
    handler()

  def handle_press(self, button):
    print('======== handle_press: ', button)
    handler = {
      "0": lambda: self._fire_turrets(),
    }.get(str(button)) or (lambda: None)
    handler()

  def handle_release(self, button):
    print('======== handle_release: ', button)
    handler = {
      "0": lambda: self._ceasefire_turrets(),
    }.get(str(button)) or (lambda: None)
    handler()

  def _handle_turning(self, data):
    print('======== turn: ', data)
    if data['direction'] == '+':
      # TODO: Turn right
      pass
    else:
      # TODO: Turn left
      pass

  def _handle_acceleration(self, data):
    print('======== accelerate: ', data)
    if data['direction'] == '+':
      # TODO: Move backward
      pass
    else:
      # TODO: Move forward
      pass

  def _handle_turret_rotation(self, data):
    print('======== rotate: ', data)
    if data['direction'] == '+':
      # TODO: Rotate CW
      pass
    else:
      # TODO: Rotate CCW
      pass

  def _handle_throttle(self, data):
    print('======== throttle: ', data)
    # TODO: Investigate wether or not we can even do something interesting with the throttle

  def _fire_turrets(self):
    print("fire!")
    self.is_firing = True

  def _ceasefire_turrets(self):
    self.is_firing = False

  def _initialize_update_thread(self):
    def set_pins_from_state():
      while True:
        sleep(.15) # Throttle this bad boy so it's not running a bajillion FPS
        # TODO: flicker turret LED if firing
        # TODO: rotate turret mount servo if rotation delta
    t = Thread(target=set_pins_from_state)
    t.start()

    return t
    
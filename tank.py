from enum import Enum
from threading import Thread
from time import sleep

class Tank:
  class Pins(Enum):
    WHEEL_RIGHT=None
    WHEEL_LEFT=None
    LED_TURRET=None
    LED_DRIVE=None
    LED_HEAD=None

  def __init__(self):
    self.is_firing = False
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

  def _handle_acceleration(self, data):
    print('======== accelerate: ', data)

  def _handle_turret_rotation(self, data):
    print('======== rotate: ', data)

  def _handle_throttle(self, data):
    print('======== throttle: ', data)

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
    
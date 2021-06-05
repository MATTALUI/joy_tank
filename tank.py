from enum import Enum

class Tank:
  class Pins(Enum):
    WHEEL_RIGHT=None
    WHEEL_LEFT=None
    LED_TURRET=None
    LED_DRIVE=None
    LED_HEAD=None

  def __init__(self):
    pass

  def handle_movement(self, data):
    print('======== move: ', data)

  def handle_press(self, button):
    print('======== handle_press: ', button)
    handler = {
      "0": lambda: self._fire_turrets(),
    }.get(str(button)) or (lambda: None)
    handler()

  def handle_release(self, button):
    print('======== handle_release: ', button)

  def _handle_turning(self):
    pass

  def _handle_acceleration(self):
    pass

  def _handle_turret_rotation(self):
    pass

  def _fire_turrets(self):
    print("fire!")
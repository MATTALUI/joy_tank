from enum import IntEnum
from threading import Thread
from time import sleep
from gpiozero import LED, Servo

class Tank:
  class Pins(IntEnum):
    SERVO_RIGHT=23
    SERVO_LEFT=22
    SERVO_TURRET=27
    LED_TURRET=17
    #LED_DRIVE=None
    #LED_HEAD=None

  def __init__(self):
    self.turret_delta = 0.0

    self.turret_led = LED(self.Pins.LED_TURRET)
    self.turret_mount = Servo(self.Pins.SERVO_TURRET, min_pulse_width=0.75/1000, max_pulse_width=2.25/1000, frame_width=20/1000)
    self.turret_mount.value = 0.0
    # self.head_led = LED(self.Pins.LED_HEAD)
    # self.drive_led = LED(self.Pins.LED_DRIVE)
    self.left_wheel = Servo(self.Pins.SERVO_LEFT, min_pulse_width=0.75/1000, max_pulse_width=2.25/1000, frame_width=20/1000)
    self.right_wheel = Servo(self.Pins.SERVO_RIGHT, min_pulse_width=0.75/1000, max_pulse_width=2.25/1000, frame_width=20/1000)
    self.update_thread = self._initialize_update_thread()
    self.left_wheel.value = None
    self.right_wheel.value = None

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
    speed = None
    if data['power'] == 'OFF':
        self.left_wheel.value = speed
        self.right_wheel.value = speed
        return
    if data['power'] == 'LOW':
        speed = 1/75
    elif data['power'] == 'HIGH':
        speed = 1

    if data['direction'] == '+':
        self.right_wheel.value = None
        self.left_wheel.value = speed
    else:
        self.right_wheel.value = -speed
        self.left_wheel.value = None

  def _handle_acceleration(self, data):
    speed = None
    if data['power'] == 'OFF':
        self.left_wheel.value = speed
        self.right_wheel.value = speed
        return
    elif data['power'] == 'LOW':
        speed = 1/75
    elif data['power'] == 'HIGH':
        speed = 1

    if data['direction'] == '+':
        # Ideally, we could use the speed var here, but the motors are slightly
        # different and the right motor doesn't seem to handle the backwards
        # power levels correctly.
        self.left_wheel.value = -1
        self.right_wheel.value = 1
    else:
        self.left_wheel.value = speed
        self.right_wheel.value = -speed

  def _handle_turret_rotation(self, data):
    power = data['power']
    new_delta = 0
    if power == 'LOW':
        new_delta = 0.01
    elif power == 'HIGH':
        new_delta = 0.05
    if data['direction'] == '+':
      # TODO: Rotate CW
      new_delta = -new_delta
    self.turret_delta = new_delta

  def _handle_throttle(self, data):
    print('======== throttle: ', data)
    # TODO: Investigate wether or not we can even do something interesting with the throttle

  def _fire_turrets(self):
    self.turret_led.blink(on_time=1/15, off_time=1/12)

  def _ceasefire_turrets(self):
    self.is_firing = False
    self.turret_led.off()

  def _initialize_update_thread(self):
    def set_pins_from_state():
      while True:
        sleep(.01) # Throttle this bad boy so it's not running a bajillion FPS
        next_value = self.turret_mount.value + self.turret_delta
        if (next_value < 1.0) and (next_value > -1.0):
            self.turret_value = next_value
            self.turret_mount.value += self.turret_delta
    t = Thread(target=set_pins_from_state)
    t.start()

    return t
    

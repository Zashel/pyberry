#!/usr/bin/python3

from RPi import GPIO
import time

class SimpleOutDevice():
    def __init__(self, board_pin, reversed=False):
        self._pin = board_pin
        self._reversed = reversed
        self._is_on = False
        self.initialize()

    def initialize(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.set_off()

    def __del__(self):
        GPIO.output(self.pin, GPIO.LOW)
        GPIO.setup(self.pin, GPIO.IN)


    @property
    def pin(self):
        return self._pin

    @property
    def reversed(self):
        return self._reversed

    @property
    def gpio(self):
        return GPIO

    @property
    def on(self):
        if self.reversed is False:
            return GPIO.HIGH
        else:
            return GPIO.LOW

    @property
    def off(self):
        if self.reversed is False:
            return GPIO.LOW
        else:
            return GPIO.HIGH

    @property
    def is_on(self):
        return self._is_on

    def commute(self):
        if self.is_on is True:
            self.set_off()
        else:
            self.set_on()

    def reverse(self):
        self._reversed = not self.reversed

    def set_on(self):
        GPIO.output(self.pin, self.on)
        self._is_on = True

    def set_off(self):
        GPIO.output(self.pin, self.off)
        self._is_on = False

    def set_status(self, status):
        if self.reversed is True:
            status = not status
        GPIO.output(self.pin, status)
        self._is_on = status and True or False

class Led(SimpleOutDevice):
    def __init__(self, board_pin):
        super().__init__(board_pin, True)

class PWMDevice(SimpleOutDevice):
    def __init__(self, board_pin=12, freq=1000):
        self._value = 0
        super().__init__(board_pin)
        self._pwm_pin = GPIO.PWM(board_pin, freq)
        self._pwm_pin.start(self._value)
        self.set_off()
    
    def initialize(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)

    def __def__(self):
        self.set_off
        self.pwm_pin.stop()
        super().__del__() 

    @property
    def pwm_pin(self):
        return self._pwm_pin

    @property
    def value(self):
        return self._value

    def set_value(self, value, step=1, t=1):
        self._value, old_value = value, self._value
        if old_value > value:
            step = -1 * step
        for x in range(old_value, value+step, step):
            self.pwm_pin.ChangeDutyCycle(x)
            time.sleep(float(t)*(abs(step)/100))
    
    def set_off(self, step=1, t=1):
        self.set_value(0, step, t)
        self._is_on = False
   
    def set_on(self, step=1, t=1):
        self.set_value(100, step, t)
        self._is_on = True

    def set_status(self, status, step=1, t=1):
        self.set_value(self, status, step, t)

    def commute(self, step=1, t=1):
        if self._is_on is True:
            self.set_off(step, t)
        else:
            self.set_on(step, t)

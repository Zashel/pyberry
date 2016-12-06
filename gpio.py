#!/usr/bin/python3

from RPi import GPIO

class SimpleOutDevice():
    def __init__(self, board_pin, reversed=False):
        self._pin = board_pin
        self._reversed = reversed
        self._is_on = False
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
        print("{}".format(self.is_on))
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

class Led(SimpleOutDevice):
    def __init__(self, board_pin):
        super().__init__(board_pin, True)
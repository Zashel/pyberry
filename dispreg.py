#!/bin/python3

from collections import deque
from RPi.GPIO import *
from zashel.utils import daemonize
import time

setmode(BOARD)

class SN74HC595():
  def __init__(self, sh_cp, st_cp, ds, oe, mr, *, bits=8, timing=64, reversed=False):
    self.sh_cp = sh_cp
    self.st_cp = st_cp
    self.ds = ds
    self.oe = oe
    self.mr = mr
    self.bits = bits
    self.timing = timing
    self.buffer = deque()
    self.reversed = reversed
    self.executing = True

  def __del__(self):
    self.executing = False
    for pin in (
        self.sh_cp,
        self.st_cp,
        self.ds,
        self.oe,
        self.mr):
      setup(pin, IN)

  def send(self, data): #may be bytes
    try:
      for bit in data:
        self.buffer.append(bit)
    except TypeError:
        self.buffer.append(data)

  @daemonize
  def run(self):
    setup(self.sh_cp, OUT)
    setup(self.st_cp, OUT)
    setup(self.ds, OUT)
    setup(self.oe, OUT)
    setup(self.mr, OUT)
    output(self.mr, HIGH)
    output(self.oe, HIGH)
    while self.executing:
      try:
        byte = self.buffer.popleft()
      except IndexError:
        byte = None
      bits = byte is None and 2 or self.bits+5
      for bit in range(0, bits):
        if byte is not None:
          if bit is 0:
            output(self.mr, LOW)
          elif bit is 1:
            output(self.ds, HIGH)
          elif bit in range(2, self.bits+3):
            if bit > 1:
              output(self.st_cp, HIGH)
            sbit = bit-2
            if sbit == self.bits:
              setter = 0
            else:
              setter = 0x01 & (byte >> sbit)
            if self.reversed is True:
              if setter == 1:
                setter = 0
              elif setter == 0:
                setter = 1
            print("Set byte {} to {}".format(sbit, setter))
            output(self.ds, setter)
          elif bit == list(range(0, bits))[-2]:
            output(self.ds, HIGH)
          elif bit == list(range(0, bits))[-1]:
            output(self.st_cp, HIGH)
        output(self.sh_cp, LOW)
        time.sleep(0.5/self.timing)


        output(self.st_cp, LOW)
        output(self.sh_cp, HIGH)
        if byte is not None:
          if bit == list(range(0, bits))[-2]:
            output(self.oe, LOW)
          elif bit == list(range(0, bits))[-1]:
            output(self.oe, HIGH)
        time.sleep(0.5/self.timing)
        output(self.ds, LOW)
        output(self.mr, HIGH)

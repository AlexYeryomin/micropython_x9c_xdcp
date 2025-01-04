# Copyright (c) 2025 Alex Yeryomin
#
# A library for MicroPython to control digital potentiometers of X9C family
# (X9C102, X9C103, X9C104, X9C503). The 'wiper' position is
# controlled by a three-wire interface.
#
# See Digitally Controlled Potentiometer (XDCP™) datasheet:
# https://www.renesas.com/en/document/dst/x9c102-x9c103-x9c104-x9c503-datasheet
#
# Note, as for the mechanical potentiometer, there is no interface
# to read the current wiper's position. The library allows
# to reset the wiper either to the lowest or the highest position.
#
# Some counterfeit/fake modules have less positions, for example,
# just 31 steps. Provide this value in the constructor.

from micropython import const
from machine import Pin
from time import sleep_us

class X9Cxxx:
    
    MAX_POSITION = const(99)
    
    DIRECTION_UP   = const(1)
    DIRECTION_DOWN = const(-1)

    def __init__(self, csPin, incPin, udPin, reset=True, direction=DIRECTION_DOWN, maxPosition=MAX_POSITION):
        self.csPin = Pin(csPin, Pin.OUT, value=1)
        self.incPin = Pin(incPin, Pin.OUT, value=1)
        self.udPin = Pin(udPin, Pin.OUT, value=0)
        self.maxPosition = maxPosition
        self._position = -1
        if reset:
            # The digital pot doesn't report its stored value.
            # Reset to the specified position.
            self.reset(direction)
    
    @property
    def waperPosition(self):
        return self._position
    
    @waperPosition.setter
    def waperPosition(self, position):
        position = X9Cxxx.constrain(position, 0, self.maxPosition)
        if self._position < 0:
            self.reset()
        if self._position > position:
            self.decrease(self._position - position)
        elif self._position < position:
            self.increase(position - self._position)
        
    def reset(self, direction=DIRECTION_DOWN):
        if direction == X9Cxxx.DIRECTION_DOWN:
            self.decrease(self.maxPosition)
            self._position = 0
        else:
            self.increase(self.maxPosition)
            self._position = self.maxPosition

    def change(self, direction, amount):
        amount = X9Cxxx.constrain(amount, 0, self.maxPosition)
        self.udPin(1 if direction > 0 else 0)
        self.incPin(1)
        self.csPin(0)
        for _ in range(amount):
            self.incPin(0)
            sleep_us(2) # Practically, unnecessary due low uPython speed.
            self.incPin(1)
            sleep_us(2) # Practically, unnecessary due low uPython speed.
            if self._position >= 0:
                  self._position += direction
        self.csPin(1)
        self._position = X9Cxxx.constrain(self._position, 0, self.maxPosition)

    def increase(self, amount=1):
        self.change(X9Cxxx.DIRECTION_UP, amount)

    def decrease(self, amount=1):
        self.change(X9Cxxx.DIRECTION_DOWN, amount)

    @staticmethod
    def constrain(x, out_min, out_max):
        return max(out_min, min(x, out_max))

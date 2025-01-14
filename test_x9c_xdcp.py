# Copyright (c) 2025 Alex Yeryomin
# The demo program to use a library to control digital
# potentiometers of X9C family (X9C102, X9C103, X9C104, X9C503).

from machine import ADC
from time import sleep
from x9c_xdcp import X9Cxxx

# Replace pin's numbers as per your schematics.
csPin, incPin, udPin = 20, 19, 18

# Some counterfeit/fake modules have less positions, for example,
# just 31 steps. Only if you have such a fake module, provide this
# value in the constructor.
MAX_POSITION = 31

adc = ADC(0)
ADC_TO_V_SCALE = 3.3 / 65535 # The scale for Pi Pico (RP2040). 

# Reset the potentiometer to the lower resistance. In case of voltage
# divider, you should get a voltage close to V(L).
pot = X9Cxxx(csPin, incPin, udPin)
print(f"Waper position: {pot.waperPosition}, V={adc.read_u16() * ADC_TO_V_SCALE}")

# Reset the potentiometer to the highest resistance. In case of voltage
# divider, you should get a voltage close to V(H).
pot = X9Cxxx(csPin, incPin, udPin, direction=X9Cxxx.DIRECTION_UP, maxPosition=MAX_POSITION)
print(f"Waper position: {pot.waperPosition}, V={adc.read_u16() * ADC_TO_V_SCALE}")


# Wiper sweep test.
direction = None
while True:
    print(f"Waper position: {pot.waperPosition}, V={adc.read_u16() * ADC_TO_V_SCALE}")
    sleep(0.1)

    if pot.waperPosition == 0:
        direction = X9Cxxx.DIRECTION_UP
    elif pot.waperPosition == MAX_POSITION:
        direction = X9Cxxx.DIRECTION_DOWN
    pot.change(direction, 1)

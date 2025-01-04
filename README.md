A library for MicroPython to control digital potentiometers of X9C family (X9C102, X9C103, X9C104, X9C503) from Renesas Electronics Corporation. See Digitally Controlled Potentiometer (XDCP™) datasheet:
https://www.renesas.com/en/document/dst/x9c102-x9c103-x9c104-x9c503-datasheet

The 'wiper' position is controlled by a three-wire interface. Note, as for the mechanical potentiometer, there is no interface to read the current wiper's position. The library allows to reset the wiper either to the lowest or the highest position.

Some counterfeit/fake modules have less positions, for example, just 31 steps. Provide this value in the constructor if needed.

Connect X9C module to a microcontroller. You don't need the lever shifter, the module works with 3.3V directly from the microcontroller. Upload the file 'x9c_xdcp.py' to a microcontroller and run the test program 'test_x9c_xdcp.py'. 

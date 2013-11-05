# Import original GPIO as _GPIO because we define our own GPIO later
from RPi import GPIO as _GPIO

# Exception to be thrown when trying to control a non-GPIO pin
class NoSuchGPIO(Exception):
    pass

# GPIO class, reduced to what we need for Floppi-Music
class GPIO:
    # All pins that are GPIO pins
    _gpios = (3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26)

    # Constructor
    def __init__(self):
        # Set GPIO mode to native Broadcom
        _GPIO.setmode(_GPIO.BOARD)

        # Setup all pins as output
        for pin in _gpios:
            _GPIO.setup(pin, _GPIO.OUT)

    # Set a selected pin high, by native board pin number
    def high(self, pin):
        if pin in _gpios:
            _GPIO.output(pin, _GPIO.HIGH)
        else:
            raise NoSuchGPIO("Pin %d is not a GPIO pin." % pin)

    # Set a selected pin low, by native board pin number
    def low(self, pin):
        if pin in _gpios:
            _GPIO.output(pin, _GPIO.LOW)
        else:
            raise NoSuchGPIO("Pin %d is not a GPIO pin." % pin)

    def toggle(self, pin):
        if pin in _gpios:
            _GPIO.output(pin, not _GPIO.input(pin))
        else:
            raise NoSuchGPIO("Pin %d is not a GPIO pin." % pin)

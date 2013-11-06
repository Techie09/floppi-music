## @package floppi.rpi
#  Wrapper for RPi.GPIO, reduced to what we need

# Copyright © 2013
#       Dominik George <nik@naturalnet.de>
#       Eike Tim Jesinghaus <eike@naturalnet.de>
#
# Provided that these terms and disclaimer and all copyright notices
# are retained or reproduced in an accompanying document, permission
# is granted to deal in this work without restriction, including un‐
# limited rights to use, publicly perform, distribute, sell, modify,
# merge, give away, or sublicence.
#
# This work is provided “AS IS” and WITHOUT WARRANTY of any kind, to
# the utmost extent permitted by applicable law, neither express nor
# implied; without malicious intent or gross negligence. In no event
# may a licensor, author or contributor be held liable for indirect,
# direct, other damage, loss, or other issues arising in any way out
# of dealing in the work, even if advised of the possibility of such
# damage or existence of a defect, except proven that it results out
# of said person’s immediate fault when using the work as intended.
# Import original GPIO as _GPIO because we define our own GPIO later

from RPi import GPIO as _GPIO

## Exception to be thrown when trying to control a non-GPIO pin
class NoSuchGPIO(Exception):
    pass

## GPIO class, reduced to what we need for Floppi-Music
class GPIO():
    ## @var _gpios
    #  All pins that are GPIO pins
    _gpios = (3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26)

    ## Constructor
    #
    #  Initializes the whole GPIO header as output.
    #
    #  @param self the object pointer
    def __init__(self):
        # Set GPIO mode to native Broadcom
        _GPIO.setmode(_GPIO.BOARD)

        # Setup all pins as output
        for pin in self._gpios:
            _GPIO.setup(pin, _GPIO.OUT)

    ## Set a selected pin high, by native board pin number
    #
    #  @param self the object pointer
    #  @param pin the native number of the pin to set
    #
    #  @throws NoSuchGPIO if the selected pin is not a GPIO pin
    def high(self, pin):
        if pin in self._gpios:
            _GPIO.output(pin, _GPIO.HIGH)
        else:
            raise NoSuchGPIO("Pin %d is not a GPIO pin." % pin)

    ## Set a selected pin low, by native board pin number
    #
    #  @param self the object pointer
    #  @param pin the native number of the pin to set
    #
    #  @throws NoSuchGPIO if the selected pin is not a GPIO pin
    def low(self, pin):
        if pin in self._gpios:
            _GPIO.output(pin, _GPIO.LOW)
        else:
            raise NoSuchGPIO("Pin %d is not a GPIO pin." % pin)

    ## Set a selected pin low if it was high, and high if it was low.
    #
    #  This method looks at the reported state of the pin.
    #
    #  @param self the object pointer
    #  @param pin the native number of the pin to set
    #
    #  @throws NoSuchGPIO if the selected pin is not a GPIO pin
    def toggle(self, pin):
        if pin in self._gpios:
            _GPIO.output(pin, not _GPIO.input(pin))
        else:
            raise NoSuchGPIO("Pin %d is not a GPIO pin." % pin)

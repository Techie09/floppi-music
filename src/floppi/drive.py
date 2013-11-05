from threading import Thread
from time import sleep

class MusicalFloppy(Thread):
    # Set up the drive thread
    def __init__(self, gpio, pins):
        # Store attributes
        self._gpio = gpio
        self._pin_direction = pins[0]
        self._pin_step = pins[1]

    # Run the drive thread
    def run(self):
        # Explicitly set pins high
        self._gpio.high(self._pin_direction)
        self._gpio.high(self._pin_step)

        # Go to home position, which is the middle track
        self.home()

    # Move count tracks
    def tracks(self, count):
        for i in range(count):
            self._gpio.toggle(self._pin_step)
            sleep(.002)
            self._gpio.toggle(self._pin_step)

    # Move to home position, which is the middle track
    def home(self):
        # Move 80 tracks, just to be sure
        self.tracks(80)
        # Toggle direction
        self._gpio.toggle(self._pin_direction)
        # Move 40 tracks back
        self.tracks(40)

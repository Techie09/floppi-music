## @package floppi.drive
#  Code to control a floppy drive for floppy music.

from threading import Thread
from time import sleep

## Class for controlling one musical floppy drive.
#
#  This class controls one floppy drive in its own thread,
#  so several drives can be used in parallel.
class MusicalFloppy(Thread):
    # Queue of tones to play
    _playqueue = []

    ## Constructor.
    #
    #  Set up the drive thread.
    #
    #  @param self the object pointer
    #  @param gpio reference to the GPIO object in use
    #  @param pins A tuple defining the pair of (direction, step) pins
    def __init__(self, gpio, pins):
        Thread.__init__(self)

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

        while True:
            if self._playqueue:
                tone = self._playqueue.pop(0)
                self.tone(tone[0], tone[1])

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

    # Shake the head with a certain interval, count times
    def vibrate(self, interval, count):
        for i in range(count):
            self._gpio.toggle(self._pin_step)
            sleep(interval)
            self._gpio.toggle(self._pin_step)
            self._gpio.toggle(self._pin_direction)

    # Play a certain frequency, for duration seconds
    def tone(self, freq, duration):
        self.vibrate(1.0/freq, int(freq*duration))

    # Add a toen to the play queue
    def play(self, tone):
        self._playqueue.append(tone)

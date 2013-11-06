# ~*~ coding: utf-8 ~*~

## @package floppi.drive
#  Code to control a floppy drive for floppy music.

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

from threading import Thread
from time import sleep

## Class for controlling one musical floppy drive.
#
#  This class controls one floppy drive in its own thread,
#  so several drives can be used in parallel.
class MusicalFloppy(Thread):
    ## @var _playqueue
    #  Queue of tones to play, containing tuples of (frequency, duration)

    ## @var _gpio
    #  Holds reference to the GPIO object in use

    ## @var _pin_direction
    #  Holds the native pin number of the GPIO pin connected to the
    #  DIRECTION pin of the floppy interface.

    ## @var _pin_step
    #  Holds the native pin number of the GPIO pin connected to the
    #  STEP pin of the floppy interface.

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
        self._playqueue = []

    ## Run the drive thread
    #
    #  Main loop function for the drive thread. It will set up the drive, then
    #  start playing tones from the _playqueue list.
    #
    #  @param self the object pointer
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

    ## Move the floppy head a certain number of tracks
    #
    #  @param self the object pointer
    #  @param count the number of tracks to move
    def tracks(self, count):
        for i in range(count):
            self._gpio.toggle(self._pin_step)
            sleep(.002)
            self._gpio.toggle(self._pin_step)

    ## Move to home position, which is the middle track
    #
    #  This method moves the head to the home position.
    #  Currently, this is the middle track (40), but this may
    #  change as we advance the floppy music quality.
    #
    #  @param self the object pointer
    def home(self):
        # Move 80 tracks, just to be sure
        self.tracks(80)
        # Toggle direction
        self._gpio.toggle(self._pin_direction)
        # Move 40 tracks back
        self.tracks(40)

    ## Shake the head with a certain interval
    #
    #  Moves the head back and forth some times, pausing in between.
    #  You can make sounds at certain frequencies by setting the interval
    #  to 1/freq. Adjust the duration of the vibration by setting
    #  the count to freq*duration.
    #
    #  @param self the object pointer
    #  @param interval the pause between movements, in seconds
    #  @param count how often to move the head
    def vibrate(self, interval, count):
        for i in range(count):
            self._gpio.toggle(self._pin_step)
            sleep(interval)
            self._gpio.toggle(self._pin_step)
            self._gpio.toggle(self._pin_direction)

    ## Play a certain frequency, for duration seconds
    #
    #  This method wraps the vibrate method with another form of arguments,
    #  more convenient for playing notes.
    #
    #  @param self the object pointer
    #  @param freq the frequency of the desired tone, in Hertz
    #  @param duration duration of the tone, in seconds
    def tone(self, freq, duration):
        self.vibrate(1.0/freq, int(freq*duration))

    ## Add a tone to the play queue
    #
    #  This method adds a tone to the _playqueue, so the main loop
    #  will pick it up and play it.
    #
    #  @param self the object pointer
    #  @param tone a tuple of (frequency, duration)
    def play(self, tone):
        if tone is list:
            self._playqueue.extend(tone)
        else:
            self._playqueue.append(tone)

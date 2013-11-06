# ~*~ coding: utf-8 ~*~

## @package floppi.drive
#  Code to control a floppy drive for floppy music and an engine of
#  musical floppy drives.

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

    ## @var _exit
    #  Exit flag for the thread.

    ## @var _playing
    #  Store if the drive is playing music.

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
        self._exit = False
        self._playing = False

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

        while not self._exit:
            if self._playqueue:
                tone = self._playqueue.pop(0)
                self.tone(tone[0], tone[1])
            else:
                self._playing = False

    ## Stop this thread (set the exit flag).
    #
    #  @param self the object pointer
    def stop(self):
        self._exit = True

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
        if duration == 0:
            return

        if freq == 0:
            sleep(duration)
        else:
            self.vibrate(1.0/freq, int(freq*duration))

    ## Add a tone to the play queue
    #
    #  This method adds a tone to the _playqueue, so the main loop
    #  will pick it up and play it.
    #
    #  @param self the object pointer
    #  @param tone a tuple of (frequency, duration)
    def play(self, tone):
        if type(tone) is list:
            self._playqueue.extend(tone)
        else:
            self._playqueue.append(tone)

        self._playing = True

    ## Lock until the drive has nothing more to play
    #
    #  @param self the object pointer
    def playing(self):
        while self._playing:
            pass

class MusicalFloppyEngine(Thread):
    ## @var _playqueue
    #  Queue of tracks to play, containing lists of tuples of (frequency, duration)

    ## @var _drives
    #  List of all drives in the engine.

    ## @var _exit
    #  Exit flag for the thread.

    ## Constructor.
    #
    #  Set up the engine thread.
    #
    #  @param self the object pointer
    #  @param gpio reference to the GPIO object in use
    #  @param pins a list of (direction, step) pin pairs for the drives
    def __init__(self, gpio, pins):
        Thread.__init__(self)

        # Setup all the drives
        self._drives = []
        for pair in pins:
            self._drives.append(MusicalFloppy(gpio, pair))

        self._playqueue = []
        self._exit = False

    ## Run the engine thread
    #
    #  Main loop function for the engine thread. It will set up the drives, then
    #  start playing tracks from the _playqueue list.
    #
    #  @param self the object pointer
    def run(self):
        # Start all the drive threads
        for drive in self._drives:
            drive.start()

        # Main loop
        while not self._exit:
            if self._playqueue:
                # Get one track from the queue
                track = self._playqueue.pop(0)

                # Count tracks
                trackn = 0
                while track:
                    # Assign track to drive
                    self._drives[trackn].play(track.pop(0))
                    trackn += 1

                # Wait for all drives to stop playing
                for drive in self._drives:
                    drive.playing()

        # Signal all floppy drive threads to stop
        for drive in self._drives:
            drive.stop()

        # Wait for all drive threads to end
        for drive in self._drives:
            drive.join()

    ## Stop this thread (set the exit flag).
    #
    #  @param self the object pointer
    def stop(self):
        self._exit = True

    ## Add a track to the play queue
    #
    #  This method adds a track to the _playqueue, so the main loop
    #  will pick it up and play it.
    #
    #  @param self the object pointer
    #  @param track a list of lists of (frequency, duration) tuples
    def play(self, track):
        self._playqueue.append(track)

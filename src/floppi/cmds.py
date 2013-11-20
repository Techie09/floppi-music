# ~*~ coding: utf-8 ~*~

## @package floppi.cmds
#  Script entry points for use by setuptools.

# Copyright © 2013
#       Dominik George <nik@naturalnet.de>
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

from sys import argv
from floppi.music import get_music_parser
from floppi.drive import MusicalFloppyEngine
from floppi.rpi import GPIO
from floppi.config import drives

## Entry point for playing a single file
#
#  The function will determine the file type, parse it with the
#  correct parser and then hand the result off to a MusicalFloppyEngine.
#
#  TODO: Print metadata
#  TODO: Multiple files
#
#  @return 0 on success, >0 on error
def play():
    def usage():
        print("Usage: %s PATH" % argv[0])
        print("")
        print("   PATH      -    Path to the file to play")

    if len(argv) != 2:
        usage()
        return 1

    # Find parser and call it
    parser = get_music_parser(argv[1])
    voices = parser(argv[1])

    # Start engine
    engine = MusicalFloppyEngine(GPIO(), drives)
    engine.start()

    # Enqueue playback
    engine.play(voices)

    # Wait for engine to get finished or Ctrl-C
    while engine is not None:
        try:
            engine.join(1)
        except KeyboardInterrupt:
            engine.stop()
            engine.join()
            engine = None

    return 0

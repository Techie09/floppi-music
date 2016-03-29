# ~*~ coding: utf-8 ~*~

## @package floppi.cmds
#  Script entry points for use by setuptools.

# Copyright © 2013
#       Dominik George <nik@naturalnet.de>
#       mirabilos <m@mirbsd.org>
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

import argparse
import pkg_resources
from sys import stderr
from floppi.music import get_music_parser
from floppi.drive import MusicalFloppyEngine
from floppi.rpi import GPIO
from floppi.config import drives

# Banner content for all commands
_banner= [
          "Copyright (c) 2013, Dominik George <nik@naturalnet.de>",
          "              2013, Eike Tim Jesinghaus <eike@naturalnet.de>",
          "Published under The MirOS Licence"
         ]

## Entry point for playing a single file
#
#  The function will determine the file type, parse it with the
#  correct parser and then hand the result off to a MusicalFloppyEngine.
#
#  TODO: Multiple files
#
#  @return 0 on success, >0 on error
def play():
    # Parse arguments
    aparser = argparse.ArgumentParser()
    aparser.add_argument("path", help="path to the file to play")
    aparser.add_argument("-q", "--quiet", help="suppress status, metadata and other output to stderr", action="store_true")
    aparser.add_argument("-v", "--visual", help="put engine in visual instead of loud mode", action="store_true")
    args = aparser.parse_args()

    # Print banner
    if not args.quiet:
        pkg = pkg_resources.require("Floppi-Music")[0]
        stderr.write("Floppi-Music File Player v%s\n" % pkg.version)
        for l in _banner:
            stderr.write("%s\n" % l)
        stderr.write("\n")
        stderr.write("Playing file: %s\n" % args.path)

    # Find parsers and call it
    try:
        parser, mparser = get_music_parser(args.path)
        if not args.quiet:
            stderr.write("Trying parser: %s\n" % parser.__name__)
    except:
        stderr.write("\nNo parser found!\n")
        return 1

    try:
        meta = mparser(args.path)
        voices = parser(args.path)
    except:
        stderr.write("\nFailed to parse with %s!\n" % parser.__name__)
        return 2

    # Print metadata if not quiet
    if not args.quiet:
        stderr.write("\n")
        metamaxlen = max([len(k.capitalize().decode('utf-8')) for k in meta])
        for k in meta:
            stderr.write(("    %" + str(metamaxlen) + "s: %s\n") % \
              (k.capitalize(), meta[k]))
        stderr.write("\n")

    # Start engine
    engine = MusicalFloppyEngine(GPIO(), drives, (1 if args.visual else 0))
    engine.start()

    # Enqueue playback
    engine.play(voices)

    # Playback time counter
    ptime = 0

    # Wait for engine to get finished or Ctrl-C
    while engine is not None and engine.isAlive():
        try:
            stderr.write("Playback time: {0:02d}:{1:05.2f} / {2:02d}:{3:05.2f}\r".format(int(ptime / 60), ptime % 60, int(meta["duration"] / 60), meta["duration"] % 60))
            engine.join(1)
            ptime += 1
        except KeyboardInterrupt:
            stderr.write("\n")
            engine.stop()
            engine.join()
            engine = None

    return 0

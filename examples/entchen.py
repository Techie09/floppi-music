#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~

from floppi.music import mml
from floppi.rpi import GPIO
from floppi.drive import MusicalFloppy

floppy = MusicalFloppy(GPIO(), (3, 5))
floppy.start()
floppy.play(mml("cdefg2g2aaaag1aaaag1ffffe2e2ddddc1"))

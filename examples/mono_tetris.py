#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~

from floppi.music import mml
from floppi.rpi import GPIO
from floppi.drive import MusicalFloppy

floppy = MusicalFloppy(GPIO(), (3, 5))
floppy.start()
floppy.play(mml("t240e2o3bo4cd2co3ba2ao4ce2dco3b2bo4cd2e2c2o3a2a1o4d2fa2gec2o3bc2"))

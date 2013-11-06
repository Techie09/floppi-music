from floppi.drive import MusicalFloppyEngine
from floppi.rpi import GPIO
from floppi.music import mml

e = MusicalFloppyEngine(GPIO(), [(3,5),(11,13),(15,19),(21,23)])
e.start()

a = mml("t84 p1      p1   f+edc+o3  babo4c+ dc+o3ba  gf+ge     o4do3abf+     gdga      >dabf+          gdga            l16o4dcdo3dcaef+do4dc<bcf+ab gf+egf+edc+o3bagf+egf+e def+gaeagf+bagagf+e            d<bbo4c+dc+o3bagf+ebabag l8f+o4f+e4p8cf+4               l4babo5c")
b = mml("t84 do3abf+ gdga o4do3abf+ gdp2    o4f+edc+ o3babo4c+ dc+o3ba       gf+ge     l8df+agf+df+e   d<bdagbag       f+deo4c+df+ao3a              bgaf+do4dd.c+16         l16dc+do3dc+aef+do4dc+<bc+f+ab gf+egf+edc+o3bagf+egf+e  def+gaeagf+bagagf+e            d<bbo4c+dc+o3bagf+ebabag")
c = mml("t84 do3abf+ gdga o4do3abf+ gdp2    o4f+edc+ gdp2      o4f+edc+      o3babo4c+ dc+o3ba         gf+ge           l8df+agf+df+e                d<bdagbag               f+deo4c+df+ao3a                bgaf+do4dd.c+16          l16dc+do3dc+aef+do4dc+<bc+f+ab gf+egf+edc+o3bagf+egf+e")
d = mml("t84 do3abf+ gdga o4do3abf+ gdp2    o4f+edc+ gdga      l8df+agf+df+e d<bdagbag f+deo4c+df+ao3a bgaf+do4dd.c+16 l4do3abf+                    gdga                    >dabf+                         gdga                     >dabf+                         gdga")

e.play([a,b,c,d])

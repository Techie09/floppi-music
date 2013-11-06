from floppi.drive import MusicalFloppyEngine
from floppi.rpi import GPIO
from floppi.music import mml

e = MusicalFloppyEngine(GPIO(), [(3,5),(11,13),(15,19),(21,23)])
e.start()

a = mml("t84 p1      p1   f+edc+o3  babo4c+ dc+o3ba  gf+ge     o4do3abf+     gdga      >dabf+          gdga            l16o4dc+do3dc+aef+do4dc+<bc+f+ab gf+egf+edc+o3bagf+egf+e def+gaeagf+bagagf+e            d<bbo4c+dc+o3bagf+ebabag l8f+o4f+e4p8c+f+4              l4babo5c+                l8do4dl4c+p8<b8d    d.l8ddgda                l16amlf+32g32mnamll32f+gmnamlo3abo4c+def+gmnf+16mldemnf+16mlo3f+gabagaf+ga mng16mlbag16f+ef+edef+gabmng16mlbamnb16o4c+do3abo4c+def+ga mnf+16mldemnf+16mledec+def+edc+mnd16ml<bc+mnd16o3mldef+gf+emnf+o4dc+d")
b = mml("t84 do3abf+ gdga o4do3abf+ gdp2    o4f+edc+ o3babo4c+ dc+o3ba       gf+ge     l8df+agf+df+e   d<bdagbag       f+deo4c+df+ao3a                  bgaf+do4dd.c+16         l16dc+do3dc+aef+do4dc+<bc+f+ab gf+egf+edc+o3bagf+egf+e  def+gaeagf+bagagf+e            d<bbo4c+dc+o3bagf+ebabag f+8o4f+8ep8d8f+     babo5c+                  d8o4d8c+p8<b8d                                                             d.l8ddgda                                                  d16mll32f+gmna16mlf+gmnao3mlabo4c+def+gmnf+16mldemnf+16o3mlf+gabagaf+ga")
c = mml("t84 do3abf+ gdga o4do3abf+ gdga    >dabf+   gdp2      o4f+edc+      o3babo4c+ dc+o3ba         gf+ge           l8df+agf+df+e                    d<bdagbag               f+deo4c+df+ao3a                bgaf+do4dd.c+16          l16dc+do3dc+aef+do4dc+<bc+f+ab gf+egf+edc+o3bagf+egf+e  def+gaeagf+bagagf+e d<bbo4c+dc+o3bagf+ebabag l4f+8o4f+8ep8d8f+                                                          babo5c                                                     d8o4d8cp8<b8d")
d = mml("t84 do3abf+ gdga o4do3abf+ gdga    >dabf+   gdga      l8df+agf+df+e d<bdagbag f+deo4c+df+ao3a bgaf+do4dd.c+16 l4do3abf+                        gdga                    >dabf+                         gdga                     >dabf+                         gdga                     >dabf+              gdga                     >dabf+                                                                     gdga                                                       >dabf+")

e.play([a,b,c,d])

# ~*~ coding: utf-8 ~*~

## @package floppi.music
#  Functions and code to parse various input formats into
#  (frequency, duration) tuples for floppi.drive.MusicalFloppy.tone .
#
#  All functions take different input formats, but return a list
#  of (frequency, duration) tuples, suitable for passing to
#  floppi.drive.MusicalFloppy.play .

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
# Import original GPIO as _GPIO because we define our own GPIO later

_notes = []
_freq = 16.35
while len(_notes) < 84:
    _notes.append(_freq)
    _freq *= pow(2, 1.0/12)
_freq = None

## Parse a string in the "music macro language"
#
#  Description of the musical macro language
#  =========================================
#
#  Taken from http://www.antonis.de/qbebooks/gwbasman/play.html .
#
#  A-G [#,+,-]
#  -----------
#  A-G are notes. # or + following a note produces a sharp; - produces a
#  flat.
#
#  L(n)    
#  ----
#  Sets the length of each note. L4 is a quarter note, L1 is a whole
#  note, and so on. n may be from 1 to 64. Length may also follow the
#  note to change the length for that note only. A16 is equivalent to
#  L16A.
#
#  MN
#  --
#  Music normal. Each note plays seven-eighths of the time determined by
#  L (length).
#
#  ML
#  --
#  Music legato. Each note plays the full period set by L.
#
#  MS
#  --
#  Music staccato. Each note plays three-quarters of the time determined
#  by L.
#
#  N(n)
#  ----
#  Play note n. n may range from 0 to 84. In the 7 possible octaves,
#  there are 84 notes. n set to 0 indicates a rest.
#
#  O(n)
#  ----
#  Octave 0 sets the current octave. There are 7 octaves (0 through 6).
#  Default is 4. Middle C is at the beginning of octave 3.
#
#  P(n)
#  ----
#  Pause. P may range from 1-64.
#
#  T(n)
#  ----
#  Tempo. T sets the number of L4s in a minute. n may range from 32-255.
#  Default is 120.
#
#  . (period)
#  ----------
#  A period after a note increases the playing time of the note by 3/2
#  times the period determined by L (length of note) times T (tempo).
#  Multiple periods can appear after a note, and the playing time is
#  scaled accordingly. For example, A. will cause the note A to play one
#  and half times the playing time determined by L (length of the note)
#  times T (the tempo); two periods placed after A (A..) will cause the
#  note to be played at 9/4 times its ascribed value; an A with three
#  periods (A...) at 27/8, etc. Periods may also appear after a P
#  (pause), and increase the pause length as described above.
#
#  >n
#  --
#  A greater-than symbol preceding the note n plays the note in the next
#  higher octave.
#
#  <n
#  --
#  A less-than symbol preceding the note n plays the note in the next
#  lower octave.
#
#
#  Example
#  =======
#
#  The German children's song "Alle meine Entchen" in music macro
#  language would be:
#
#  c d e f g2 g2 a a a a g1 a a a a g1 f f f f e2 e2 d d d d c1
#
#
#  @param macro string in the music macro language
#  @return a list of (frequency, duration) tuples
def mml(macro):
    res = []

    # State machine variables
    bpm = 120
    current_c = 48
    part = 7.0/8
    length = 60.0 / bpm

    # Normalize macro string
    macro = macro.upper()
    macro = macro.replace(" ", "")
    macro = list(macro)

    while macro:
        char = macro.pop(0)

        if char in ("C", "D", "E", "F", "G", "A", "B"):
            if char == "C":
                note = current_c
            elif char == "D":
                note = current_c + 2
            elif char == "E":
                note = current_c + 4
            elif char == "F":
                note = current_c + 5
            elif char == "G":
                note = current_c + 7
            elif char == "A":
                note = current_c + 9
            elif char == "B":
                note = current_c + 11

            if macro and macro[0] in ("#", "+"):
                note += 1
                macro.pop(0)
            elif macro and macro[0] == "-":
                note -= 1
                macro.pop(0)

            n = ""
            while macro and macro[0] in [str(x) for x in range(10)]:
                n += macro.pop(0)

            _length = length
            if n:
                _length = 60.0 / bpm * 4 / float(n)

            res.append((_notes[note], _length * part))
            res.append((0, _length - _length * part))
        elif char == "O":
            n = ""
            while macro and macro[0] in [str(x) for x in range(10)]:
                n += macro.pop(0)
            current_c = int(n) * 12

    return res

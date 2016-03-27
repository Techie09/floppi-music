# ~*~ coding: utf-8 ~*~

## @package floppi.music
#  Functions and code to parse various input formats into
#  (frequency, duration) tuples for floppi.drive.MusicalFloppy.tone .
#
#  All functions take different input formats, but return a list
#  of (frequency, duration) tuples, suitable for passing to
#  floppi.drive.MusicalFloppy.play .

# Copyright © 2016
#       mirabilos <m@mirbsd.org>
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

from __future__ import with_statement

## Pre-calculated note frequencies
#
#  The list comprehension creates a list of 84 frequencies
#  from C2 (C, o0c) to B8 (h''''', o6b).
_notes = [(440.0 * pow(2, (n - 33) / 12.)) for n in xrange(0, 84)]

## Note offsets
#
#  Map note names to half-tone steps from the current C
_noteoffsets = { "C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11 }

## Calculate playback length of a list of (frequency, duration) tuples
#
#  This function looks at all the tuples in a playback list and estimates
#  the playback duration by adding up the durations.
#
#  @param track the track list
#  @return the estimated duration in seconds
def estimate_duration(track):
    # Remove all non-tuples from the list; integer 1 is abused by mml_parse
    # for syncmarks; extract second entries of tuples and add them up and
    # return the result, all in one list comprehension -- I ❤ Python!
    return sum([x[1] for x in track if type(x) is tuple])

## Play a note or pause
#
#  Helper function to play an MML note after parsing sustain dots
#
#  @param macro the MML list
#  @param res the result list
#  @param bpm the current tempo
#  @param art the current articulation
#  @param note the note number minus 1, or -1 for pause
#  @param length the time value (length) to play
def _play(macro, res, bpm, art, note, length):
    # parse sustain dots
    while macro and macro[0] == ".":
        macro.pop(0)
        length /= 1.5

    # calculate duration
    duration = ((60.0 / bpm) * 4) / length

    # articulate note
    if note == -1:
        # pause
        res.append((0, duration))
    elif art == 'L':
        # legato
        res.append((_notes[note], duration))
    else:
        # normal or staccato
        if art == 'N':
            part = 7.0/8
        else:
            part = 3.0/4
        res.append((_notes[note], duration * part))
        res.append((0, duration - duration * part))

## Parse an MML number
#
#  Parses an MML number (positive) with bounds checking
#
#  @param macro the MML list
#  @param minval the minimum allowed value
#  @param maxval the maximum allowed value
#  @param defval the default value to use if bounds are exceeded
#  @return an int, or defval
def _getint(macro, minval, maxval, defval):
    n = ""
    while macro and macro[0].isdigit():
        n += macro.pop(0)
    if not n:
        return defval
    i = int(n)
    if i < minval or i > maxval:
        return defval
    return i

## Parse a string in the "music macro language"
#
#  Based on the documentation in: https://www.mirbsd.org/man4/spkr
#
#  Description of the musical macro language
#  =========================================
#
#  Based on http://www.antonis.de/qbebooks/gwbasman/play.html .
#
#  A-G[#,+,-][length]
#  ------------------
#  A-G are notes. # or + following a note produces a sharp; - produces a
#  flat.
#
#  L(n)
#  ----
#  Sets the length of each note. L4 is a quarter note, L1 is a whole
#  note, and so on. n may be from 1 to 64. Length may also follow the
#  note to change the length for that note only. A16 is equivalent to
#  L16A. Default is L4.
#
#  ML
#  --
#  Music legato. Each note plays the full period set by L.
#
#  MN
#  --
#  Music normal. Each note plays seven-eighths of the time determined by
#  L (length).
#
#  MS
#  --
#  Music staccato. Each note plays three-quarters of the time determined
#  by L.
#
#  N(n)
#  ----
#  Play note n. n may range from 0 to 84. In the 7 possible octaves,
#  there are 84 notes. n set to 0 (or omitted) indicates a rest.
#
#  O(n)
#  ----
#  Octave 0 sets the current octave. There are 7 octaves (0 through 6).
#  Default is 4. Middle C is at the beginning of octave 2.
#
#  P(n)
#  ----
#  Pause. n may range from 1-64; the current L value is used if omitted.
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
#  >
#  -
#  A greater-than symbol raises the current octave by one.
#
#  <
#  -
#  A less-than symbol lowers the current octave by one.
#
#  |
#  -
#
#  Optionally used as a synchronisation mark for multi-track music.
#  This is a proprietary extension in the Floppi-Music project.
#
#
#  Example
#  =======
#
#  The German children's song "Alle meine Entchen" in music macro
#  language would be:
#
#  o2 c d e f g2 g2 a a a a g1 a a a a g1 f f f f e2 e2 d d d d c1
#
#
#  @param macro string in the music macro language
#  @return a list of (frequency, duration) tuples
def mml(macro):
    res = []

    # State machine variables
    art = 'N'
    bpm = 120
    octave = 4
    timevalue = 4

    # Normalise macro string
    macro = macro.upper()
    macro = macro.replace(" ", "")
    macro = list(macro)

    while macro:
        char = macro.pop(0)

        if char in _noteoffsets.keys():
            # base note
            note = 12 * octave + _noteoffsets[char]

            # accidental sign
            if macro and macro[0] in ("#", "+"):
                if note < 83:
                    note += 1
                macro.pop(0)
            elif macro and macro[0] == "-":
                if note > 0:
                    note -= 1
                macro.pop(0)

            # length
            _length = _getint(macro, 1, 64, timevalue)

            # sustain dots, and play the note
            _play(macro, res, bpm, art, note, _length)

        elif char == "L":
            timevalue = _getint(macro, 1, 64, 4)

        elif char == "M":
            if macro:
                char = macro.pop(0)
                if char in ("L", "N", "S"):
                    art = char

        elif char == "N":
            # n > 84 causes an IndexError; BSD skips the command silently
            note = _getint(macro, 0, 84, -1) - 1
            _play(macro, res, bpm, art, note, timevalue)

        elif char == "O":
            octave = _getint(macro, 0, 6, 4)

        elif char == "P":
            _length = _getint(macro, 1, 64, timevalue)
            _play(macro, res, bpm, art, -1, _length)

        elif char == "T":
            bpm = _getint(macro, 32, 255, 120)

        elif char == "<":
            if octave > 0:
                octave -= 1

        elif char == ">":
            if octave < 6:
                octave += 1

        elif char == "|":
            if len(res) == 0 or res[-1] != 1:
                res.append(1)

        #elif char == "X":
        # consider causing an exception

    return res

## Parse a file in the music macro language
#
#  The MML file format as used by Floppi-Music is proprietary.
#
#  File format
#  ===========
#
#  Comments
#  --------
#
#  Lines starting with # are comments. At the beginning of the file,
#  comments may be used to encode metadata. This is yet to be specified.
#
#  Voices
#  ------
#  The voices of a song are interleaved. They are grouped per notation
#  system, and the notation systems are seperated by empty lines.
#
#
#  @param path the path to the MML file
#  @return a list of lists of (frequency, duration) tuples, suitable
#          for passing to the MusicalFloppyEnging
def mml_file(path):
    vstrings = []
    vlists = []
    vcount = 0

    with open(path, "r") as f:
        for l in f:
            if l.strip().startswith("#"):
                continue
            elif l.strip() == "":
                vcount = 0
            else:
                if len(vstrings) <= vcount:
                    vstrings.append("")
                vstrings[vcount] += l.strip()
                vcount += 1

    for v in vstrings:
        vlists.append(mml(v))

    return vlists

## Parse a file in the music macro language and return metadata
#
#  The MML file format as used by Floppi-Music is proprietary.
#
#  @param path the path to the MML file
#  @return a dictionary of metadata
def mml_file_meta(path):
    state = 0
    vcount = 0
    meta = {}

    with open(path, "r") as f:
        for l in f:
            if state == 0:
                # Header fields
                if l.strip() == "":
                    state = 1
                elif l.strip().startswith("# ") and ":" in l:
                    parts = l.strip()[1:].split(":")
                    key = parts.pop(0)
                    value = ":".join(parts)

                    meta[key.strip().lower()] = value.strip()
            elif state == 1:
                # Skip first space
                if not l.strip() == "":
                    state = 2
            elif state == 2:
                vcount += 1
                if l.strip() == "":
                    # Everything of interest has gone
                    break

    # Add discovered voice count to meta if not explicitly given
    if not "voices" in meta:
        meta["voices"] = vcount

    # Estimate duration of tracks and add maximum to meta if not
    # explicitly given
    if not "duration" in meta:
        meta["duration"] = max([estimate_duration(x) for x in mml_file(path)])

    return meta

## Determine the function to use to parse a given input file
#
#  This function is quite dumb right now and only uses the filename
#  extension.
#
#  @param path the path to the file to analyze
#  @return a tuple of parser and metadata parser
def get_music_parser(path):
    if path.endswith(".mml"):
        return (mml_file, mml_file_meta)

## Debugging, if directly called
#
# Parses its first argument as MML and displays the tuples.
#
if __name__ == '__main__':
    import sys
    print mml(sys.argv[1])

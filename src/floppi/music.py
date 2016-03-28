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
import codecs

## Pre-calculated note frequencies
#
#  The list comprehension creates a list of 84 frequencies
#  from C2 (C, o0c) to B8 (h''''', o6b).
_notes = [(440.0 * pow(2, (n - 33) / 12.)) for n in xrange(0, 84)]

## Note offsets
#
#  Map note names to half-tone steps from the current C
#  and back, assuming ♯ for all half-tones but B♭
_noteoffsets = { "C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11 }
_notefromofs = [ item for sublist in [ [
    ( octave, 'C', u'♮' ),
    ( octave, 'C', u'♯' ),
    ( octave, 'D', u'♮' ),
    ( octave, 'D', u'♯' ),
    ( octave, 'E', u'♮' ),
    ( octave, 'F', u'♮' ),
    ( octave, 'F', u'♯' ),
    ( octave, 'G', u'♮' ),
    ( octave, 'G', u'♯' ),
    ( octave, 'A', u'♮' ),
    ( octave, 'B', u'♭' ),
    ( octave, 'B', u'♮' ),
  ] for octave in xrange(0, 7) ] for item in sublist ];

## MusicXML note lengths
_xmlnotetypes = { 64: '64th', 32: '32nd', 16: '16th',
  8: 'eighth', 4: 'quarter', 2: 'half', 1: 'whole' }

## Calculate greatest common divisor
def ggT(a, b):
    while b:
        (a, b) = (b, a % b)
    return a

## Calculate least/lowest/smallest common multiple
def kgV(a, b):
    return (a * b) // ggT(a, b)

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

## Merge note or pause onto playlist
#
# Helper function to merge a note or pause onto the playlist
#
#  @param res the result list
#  @param freq the frequency (0 to pause)
#  @param dur the length
def _addtoplaylist(res, freq, dur):
    # simple case
    if len(res) == 0 or type(res[-1]) is not tuple:
        res.append((freq, dur))
        return
    # merge same-frequency occurrences
    prec = res.pop()
    if prec[0] == freq:
        res.append((freq, prec[1] + dur))
        return
    # oops, no; restore preceding element and add a new one
    res.append(prec)
    res.append((freq, dur))

## Add bar line to playlist
#
#  Helper function to merge a synchronisation mark onto the playlist
#
#  @param res the result list
def _addbartoplaylist(res):
    if len(res) > 0 and res[-1] != 1:
        res.append(1)

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
#  @param extra extra information for XML export
def _play(macro, res, bpm, art, note, length, extra):
    # parse sustain dots
    while macro and macro[0] == ".":
        macro.pop(0)
        length /= 1.5

    # calculate duration
    duration = ((60.0 / bpm) * 4) / length

    # articulate note
    if note == -1:
        # pause
        _addtoplaylist(res, 0, duration)
    elif art == 'L':
        # legato
        _addtoplaylist(res, _notes[note], duration)
    else:
        # normal or staccato
        if art == 'N':
            part = 7.0/8
        else:
            part = 3.0/4
        _addtoplaylist(res, _notes[note], duration * part)
        _addtoplaylist(res, 0, duration - duration * part)

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
            extra = (octave, char, u'♮')

            # accidental sign
            if macro and macro[0] in ("#", "+"):
                if note < 83:
                    note += 1
                    extra = (octave, char, u'♯')
                macro.pop(0)
            elif macro and macro[0] == "-":
                if note > 0:
                    note -= 1
                    extra = (octave, char, u'♭')
                macro.pop(0)

            # length
            _length = _getint(macro, 1, 64, timevalue)

            # sustain dots, and play the note
            _play(macro, res, bpm, art, note, _length, extra)

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
            _play(macro, res, bpm, art, note, timevalue, note)

        elif char == "O":
            octave = _getint(macro, 0, 6, 4)

        elif char == "P":
            _length = _getint(macro, 1, 64, timevalue)
            _play(macro, res, bpm, art, -1, _length, -1)

        elif char == "T":
            bpm = _getint(macro, 32, 255, 120)

        elif char == "<":
            if octave > 0:
                octave -= 1

        elif char == ">":
            if octave < 6:
                octave += 1

        elif char == "|":
            _addbartoplaylist(res)

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

    with codecs.open(path, "r", "UTF-8") as f:
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

    with codecs.open(path, "r", "UTF-8") as f:
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
            if state == 1:
                # Skip first space
                if not l.strip() == "":
                    state = 2
            if state == 2:
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
# If the first argument is the name of a *.mml file, reads it
# and outputs equivalent MusicXML.
# Otherwise, parses it as MML string and displays the tuples.
#
if __name__ == '__main__':
    import sys
    if not sys.argv[1].endswith(".mml"):
        print mml(sys.argv[1])
        sys.exit(0)

    ###################
    # MusicXML export #
    ###################

    # reuse the parser, override _addbartoplaylist (not currently needed)
    # and _addtoplaylist and/or _play (we only need _play at the moment);
    # this breaks the metadata function though, so do that first:
    meta = mml_file_meta(sys.argv[1])

    # now override the functions
    orig_play = _play
    def _play(macro, res, bpm, art, note, length, extra):
        # 'extra' can be: -1 (pause), 0‥83 (note), or a tuple
        # (mml-octave-number, note-char, u'♭' | u'♮' | u'♯')

        # parse sustain dots
        ndots = 0
        while macro and macro[0] == ".":
            macro.pop(0)
            ndots += 1

        res.append((bpm, art, length, ndots, extra))

    # call overridden functions
    staves = mml_file(sys.argv[1])

    # create MusicXML document
    import xml
    import xml.dom.minidom
    mdi = xml.dom.minidom.getDOMImplementation('')
    doc = mdi.createDocument(None, 'score-partwise',
      mdi.createDocumentType('score-partwise',
      '-//Recordare//DTD MusicXML 3.0 Partwise//EN',
      'http://www.musicxml.org/dtds/partwise.dtd'))
    score = doc.documentElement
    score.setAttribute('version', '3.0')

    # carry over floppi.music-specific metadata
    if meta.has_key('title'):
        x = doc.createElement('movement-title')
        x.appendChild(doc.createTextNode(meta['title']))
        score.appendChild(x)
        del(meta['title'])
    tmpel = doc.createElement('identification')
    if meta.has_key('composer'):
        x = doc.createElement('creator')
        x.setAttribute('type', 'composer');
        x.appendChild(doc.createTextNode(meta['composer']))
        tmpel.appendChild(x)
        del(meta['composer'])
    if meta.has_key('lyrics'):
        x = doc.createElement('creator')
        x.setAttribute('type', 'lyricist');
        x.appendChild(doc.createTextNode(meta['lyrics']))
        tmpel.appendChild(x)
        del(meta['lyrics'])
    if meta.has_key('arranger'):
        x = doc.createElement('creator')
        x.setAttribute('type', 'arranger');
        x.appendChild(doc.createTextNode(meta['arranger']))
        tmpel.appendChild(x)
        del(meta['arranger'])
    if meta.has_key('artist'):
        x = doc.createElement('creator')
        x.appendChild(doc.createTextNode(meta['artist']))
        tmpel.appendChild(x)
        del(meta['artist'])
    if meta.has_key('copyright'):
        x = doc.createElement('rights')
        x.appendChild(doc.createTextNode(meta['copyright']))
        tmpel.appendChild(x)
        del(meta['copyright'])
    tmpex = doc.createElement('encoding')
    if meta.has_key('encoder'):
        x = doc.createElement('encoder')
        x.appendChild(doc.createTextNode(meta['encoder']))
        tmpex.appendChild(x)
        del(meta['encoder'])
    x = doc.createElement('software')
    x.appendChild(doc.createTextNode('floppi.music by Nik, Eike, and mirabilos'))
    tmpex.appendChild(x)
    tmpel.appendChild(tmpex)
    if meta.has_key('source'):
        x = doc.createElement('source')
        x.appendChild(doc.createTextNode(meta['source']))
        tmpel.appendChild(x)
        del(meta['source'])
    tmpex = doc.createElement('miscellaneous')
    for tmp in meta:
        x = doc.createElement('miscellaneous-field')
        x.setAttribute('name', tmp)
        x.appendChild(doc.createTextNode(str(meta[tmp])))
        tmpex.appendChild(x)
    tmpel.appendChild(tmpex)
    score.appendChild(tmpel)

    # required metadata
    tmpel = doc.createElement('part-list')
    for trkno in xrange(1, len(staves) + 1):
        score_part = doc.createElement('score-part')
        score_part.setAttribute('id', 'P' + str(trkno))
        part_name = doc.createElement('part-name')
        part_name.appendChild(doc.createTextNode('Zeile ' + str(trkno)))
        score_part.appendChild(part_name)
        tmpel.appendChild(score_part)
    score.appendChild(tmpel)

    # figure out which duration to use
    notelens = 4
    for trkno in xrange(1, len(staves) + 1):
        for ply in staves[trkno - 1]:
            if type(ply) is tuple:
                dottedlen = ply[2]
                for tmp in xrange(0, ply[3]):
                    dottedlen *= 2
                notelens = kgV(notelens, dottedlen)
    divisions = notelens // 4

    # add individual staves
    for trkno in xrange(1, len(staves) + 1):
        staff = staves[trkno - 1]
        trknode = doc.createElement('part')
        trknode.setAttribute('id', 'P' + str(trkno))

        # attribute node, once per part, located in the first bar
        tmpel = doc.createElement('attributes')
        x = doc.createElement('divisions')
        x.appendChild(doc.createTextNode(str(divisions)))
        tmpel.appendChild(x)
        # use treble clef by default
        tmpex = doc.createElement('clef')
        x = doc.createElement('sign')
        x.appendChild(doc.createTextNode('G'))
        tmpex.appendChild(x)
        x = doc.createElement('line')
        x.appendChild(doc.createTextNode('2'))
        tmpex.appendChild(x)
        tmpel.appendChild(tmpex)

        # "current" bar node and number (first, here)
        barno = 1
        barnode = doc.createElement('measure')
        barnode.setAttribute('number', str(barno))
        barnode.appendChild(tmpel)
        # hack to always end on a bar line, so the last bar is not lost
        if len(staff) == 0 or staff[-1] != 1:
            staff.append(1)

        # now iterate through the staff
        bpm = -1
        for ply in staff:
            # finish a bar?
            if ply == 1:
                trknode.appendChild(barnode)
                # force re-init on next note
                barnode = None
                continue

            # start a new bar?
            if barnode is None:
                barno += 1
                barnode = doc.createElement('measure')
                barnode.setAttribute('number', str(barno))

            # tempo change?
            if bpm != ply[0]:
                x = doc.createElement('sound')
                x.setAttribute('tempo', str(ply[0]))
                #XXX or in a direction container node?
                barnode.appendChild(x)

            # unpack and convert raw note to pitch (best guess)
            (bpm, art, length, ndots, extra) = ply
            if type(extra) is not tuple and extra != -1:
                extra = _notefromofs[extra]

            # convert to MusicXML
            tmpel = doc.createElement('note')
            if extra == -1:
                tmpex = doc.createElement('rest')
            else:
                tmpex = doc.createElement('pitch')
                x = doc.createElement('step')
                x.appendChild(doc.createTextNode(extra[1]))
                tmpex.appendChild(x)
                if extra[2] != u'♮':
                    x = doc.createElement('alter')
                    if extra[2] == u'♭':
                        x.appendChild(doc.createTextNode('-1'))
                    elif extra[2] == u'♯':
                        x.appendChild(doc.createTextNode('1'))
                    tmpex.appendChild(x)
                x = doc.createElement('octave')
                x.appendChild(doc.createTextNode(str(extra[0] + 2)))
                tmpex.appendChild(x)
            tmpel.appendChild(tmpex)
            # if notelens calculation is correct, dottedlen is always integer
            dottedlen = notelens / length
            for tmp in xrange(0, ndots):
                dottedlen *= 1.5
            x = doc.createElement('duration')
            x.appendChild(doc.createTextNode(str(int(dottedlen))))
            tmpel.appendChild(x)
            if length in _xmlnotetypes.keys():
                x = doc.createElement('type')
                x.appendChild(doc.createTextNode(_xmlnotetypes[length]))
                tmpel.appendChild(x)
            # order is important!
            for tmp in xrange(0, ndots):
                tmpel.appendChild(doc.createElement('dot'))
            if art == 'S':
                tmpex = doc.createElement('notations')
                x = doc.createElement('articulations')
                x.appendChild(doc.createElement('staccato'))
                tmpex.appendChild(x)
                tmpel.appendChild(tmpex)
            elif art == 'L':
                #XXX
                tmpex = doc.createElement('notations')
                x = doc.createElement('articulations')
                x.appendChild(doc.createElement('detached-legato'))
                tmpex.appendChild(x)
                tmpel.appendChild(tmpex)
            barnode.appendChild(tmpel)
        score.appendChild(trknode)

    print doc.toxml("UTF-8")

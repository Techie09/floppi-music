#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~

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
# Import original GPIO as _GPIO because we define our own GPIO later

from setuptools import setup, find_packages

setup(
    # Basic information
    name             = 'Floppi-Music',
    version          = '0.01',
    license          = 'MirOS',
    long_description = 'Crazily advanced floppy music player for Raspberry Pi',
    url              = 'https://github.com/Natureshadow/floppi-music',

    # Author information
    author       = 'Dominik George, Eike Tim Jesinghaus',
    author_email = 'nik@naturalnet.de',

    # Included code
    packages             = find_packages('src'),
    package_dir          = {
                            '': 'src'
                           },
    entry_points         = {
                            'console_scripts': [
                                                'floppi-play = floppi.cmds:play'
                                               ]
                           },

    # Distribution information
    zip_safe         = False,
    install_requires = [
                        'RPi.GPIO'
                       ],
    classifiers      = [
                        'Development Status :: 3 - Alpha',
                        'Environment :: Console',
                        'Intended Audience :: Developers',
                        'Intended Audience :: Science/Research',
                        'Natural Language :: English',
                        'Operating System :: POSIX',
                        'Programming Language :: Python :: 2.7',
                        'Topic :: Artistic Software',
                        'Topic :: Multimedia :: Sound/Audio :: Players'
                       ]
)

# ~*~ coding: utf-8 ~*~

## @package floppi.config
#  Handles configuration of the floppy music engine
#
#  All configuration is hard-coded right now.
#
#  TODO: Use ConfigParser

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

## List of pins for drive control
#  
#  Hard-coded default as in doc/wiring.txt
#
#  TODO: Extend for 8 drives
drives = [(3,5),(11,13),(15,19),(21,23)]

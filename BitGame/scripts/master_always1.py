#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## master_always1.py

#############################################################################
# Copyright (C) Labomedia November 2013
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franproplin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#############################################################################

from bge import logic as gl
##from scripts.pert1 import Pert
from scripts.network1 import network_main
from scripts.note import note_main
from scripts.FPS_bit2 import FPS_main


def master_always_main():
    gl.t_start += 1
    # Get wikikirc
    network_main()
    # Get etherpad
    gl.t_pad += 1
    if gl.pad_change:
        print(gl.pad_out)

    if gl.t_start > 2:
        note_main()
        FPS_main()

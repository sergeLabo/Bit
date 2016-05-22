#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## master1.py

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
from scripts.master_init1 import master_init_main
from scripts.master_always1 import master_always_main

controller = gl.getCurrentController()
owner = controller.owner

def main():
    ''' To never relaod scripts in Blender. '''
    if not owner["once"]:
        master_init_main()
        owner["once"] = True
    else:
        master_always_main()

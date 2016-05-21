#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## FPS_bit2.py

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
from bge import render
from scripts.getblenderobject1 import GetBlenderObject

def FPS_main():
    mouse = gl.mouse

    objDict = GetBlenderObject.get()
    cam = objDict["Camera.003"]
    cylinder = objDict["me"]

    Hrot = 3 * (0.5 - mouse.position[0])
    if -0.002 < Hrot < 0.002:
        Hrot = 0
    cylinder.applyRotation([0, 0, Hrot], False)

    Vrot = 1 * (0.5 - mouse.position[1])
    if -0.001 < Vrot < 0.001:
        Vrot = 0
    cam.applyRotation([Vrot, 0, 0], True)

    # Center the mouse
    render.setMousePosition(int(render.getWindowWidth() / 2),
                                int(render.getWindowHeight() / 2))
    #print(Hrot, Vrot)

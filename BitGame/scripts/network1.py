#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## network1.py

#############################################################################
# Copyright (C) Labomedia March 2011
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

import random
from bge import logic as gl
from scripts.easyosc1 import GetOsc, SendOsc

def network_main():
    if not gl.network:
        # Get Socket
        gl.receiveOPY = GetOsc(gl.host, gl.port_in, 1024, 0.01)
        gl.network = True
        # Send Socket
        gl.sendOPY = SendOsc(verbose=False)

    # If connected
    if gl.network:
        data = gl.receiveOPY.receive()
        recup_messages(data)

        # Send to pure data example
        address = (gl.host, gl.port_out)
        title = "/blender/x"
        msg = 10 * random.random()
        gl.sendOPY.send_simple_message(address, title, msg)

def recup_messages(data):
    # ['#bundle', 0.0, ['/irc', ',s', 'test']]
    data = data[2:]
    for m in data:
        if gl.musicsources == "irc":
            if '/irc' in m:
                if gl.irc_out != m[2]:
                    gl.irc_change = True
                    gl.irc_out = m[2]
        if gl.musicsources == "pad":
            if '/pad' in m:
                if len(m[2]) > 0:
                    gl.pad_change = True
                    gl.pad_out = m[2]

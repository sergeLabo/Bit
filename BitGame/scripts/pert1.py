#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## pert1.py

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

try:
    from bge import logic as gl
except:
    pass

from time import time, sleep
from game import Game
from sometools1 import VirtualGl

class Pert(Game):
    ''' one object = one state '''
    def __init__(self, state_prev, state, state_next):
        Game.__init__(self)
        self.state_prev = state_prev
        self.state = state
        self.state_next = state_next
        self.chrono = 0
        self.zero = time()

    def update(self):
        self.chrono = time()
        print(self.chrono)

    def end(self):
        pass

def end_scene(this_scene):
    '''Delete this_scene'''
    for scn in gl.getSceneList():
        if scn.name == this_scene:
            scn.end()
            print("End of scene:", scn)

def scene_list():
    return gl.getSceneList()

if __name__ == "__main__":
    gl = VirtualGl()
    gl.pert = Pert("1", "2", "3")

    while True:
        gl.pert.update()
        sleep(1)
        print

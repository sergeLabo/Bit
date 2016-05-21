#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## master_init.py

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
from scripts.sound1 import EasyAudio


def master_init_main():
    print("Initialisation du jeu Bit de Dieu")
    print('"Bit de Dieu" is licensed under the')
    print("Creative Commons Attribution-ShareAlike 3.0 Unported License.")

    gl.debug = True
    init_variable()
    init_audio()
    init_note()

def init_variable():
    gl.t_start = 0
    gl.network = False # in network.py
    gl.host = '127.0.0.1'
    gl.port_in = 8000
    gl.port_out = 9000
    gl.irc_out = "Premier message"
    gl.pad_out = "Serviette farcie"
    gl.t_pad = 0

def init_note():
    #gl.musicsources = "pad"
    gl.musicsources = "irc"
    gl.frame_counter = 0
    gl.irc_change = False
    gl.pad_change = False
    gl.position = 0

def init_audio():
    note_list = []
    for i in range(36):
        note_list.append(str(i))
    gl.note_piano = EasyAudio(note_list, "//samples/")


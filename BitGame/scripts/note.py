#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## note.py

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

import textwrap
from bge import logic as gl
from scripts.getblenderobject1 import GetBlenderObject

note_dict = {   '0':0,  '1':35,  '2':2,  '3':34,  '4':4,  '5':33,
                'a':6,  'b':7,  'c':8,  'd':9,  'e':10, 'f':11,
                'g':12, 'h':13, 'i':14, 'j':15, 'k':16, 'l':17,
                'm':18, 'n':19, 'o':20, 'p':21, 'q':22, 'r':23,
                's':24, 't':25, 'u':26, 'v':27, 'w':28, 'x':29,
                'y':30, 'z':31, '6':32, '7':1, '8':3, '9':5}

def note_main():
    objDict = GetBlenderObject.get()
    decod = apply_irc_out(objDict)
    gl.frame_counter += 1
    # If new message, reinit
    if gl.pad_change or gl.irc_change:
        gl.position = -1
        gl.irc_change = False
        #gl.pad_change = False

    # Every "every" frame, play note
    every = 12
    if len(decod) < 30:
        every = 18
    if 31 < len(decod) < 100:
        every = 16
    if 101 < len(decod) < 200:
        every = 14
    if 201 < len(decod) < 300:
        every = 12
    if 301 < len(decod) < 400:
        every = 10
    if 400 < len(decod):
        every = 8

    if gl.frame_counter % every == 0:
        if gl.position < len(decod) -1:
            gl.position += 1
            if decod[gl.position] in list(note_dict.keys()):
                note = str(note_dict[decod[gl.position]])
                gl.note_piano[note].play()
                n = min(len(decod), 500)
                vol = 0.4 + 0.5 * n/500
                gl.note_piano[note].set_volume(vol)
                #print("gl.position", gl.position, "note", note)

def apply_irc_out(objDict):
    # gl.irc_out <type 'str'> is encode in python 3
    decod = ""
    if gl.musicsources == "pad":
        decod = gl.pad_out.encode('latin-1').decode('utf-8')
    if gl.musicsources == "irc":
        decod = gl.irc_out.encode('latin-1').decode('utf-8')

    #print(decod)

    # Display format
    objDict["TextIRC"]["Text"] = paragraphe(decod)
    objDict["TextIRC"].resolution = 64

    return decod

def paragraphe(text):
    if isinstance(text, str):
        text = textwrap.fill(text, 80)
        return text
    else:
        print("Text must be a string")

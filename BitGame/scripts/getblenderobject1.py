#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## getblenderobject.py

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

import bge

class GetBlenderObject():
    def get():
        '''
            Get all blender objects from all scenes in a dict {object.name: object}.
            Very usefull but objDict is argument in all functions.
            Example: 
                objDict = GetBlenderObject.get()
                object Cube is objDict["Cube"]

        '''
        scenes = bge.logic.getSceneList()
        objDict = {}
        for scn in scenes:
            for obj in scn.objects:
                objDict[obj.name] = obj
        return objDict

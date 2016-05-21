#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## textureChange.py

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
from bge import texture

class TextureChange():
    ''' Class to change textures in Blender Game Engine. '''

    def __init__(self, obj, old_tex):
        ''' obj     = blendr object
            old_tex = old texture
            new_tex = new texture.
        '''

        self.obj = obj
        self.old_tex = old_tex
        # Existing texture ID
        self.ID = texture.materialID(obj, 'IM' + old_tex)
        # Save python object in GameLogic
        self.obj_texture = texture.Texture(obj, self.ID)

    def texture_new(self, directory, new_tex):
        ''' Apply new texture.
            directory : set relative path
            "//" is the current directory.
        '''

        # New source
        self.url = gl.expandPath(directory + new_tex)
        self.new_source = texture.ImageFFmpeg(self.url)

        # Apply
        self.obj_texture.source = self.new_source
        self.obj_texture.refresh(False)

    def texture2old(self):
        ''' Return to old texture. '''

        self.obj_texture = texture.Texture(self.obj, self.ID)
        self.obj_texture.refresh(True)



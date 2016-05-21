#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

## bitManagement.py

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

from twisted.internet import reactor
from txosc import async, dispatch, osc
from collections import OrderedDict
from time import time, sleep

class GameManagement(object):
    def __init__(self):
        self.manage = OrderedDict()

    def cars_to_dict(self, message, address):
        # Called only with /c message
        if address in self.manage:
            self.manage[address][0] = message
            self.manage[address][1] = time()
            self.manage[address][2] = self.manage.keys().index(address)
        else:
            # position on starting line = position in OrderedDict
            # 0 to 3: 0 run with car00, ...
            position = len(self.manage)
            if position > 3:
                self.reset_data()
                print "Too much players, only 4"
            # Create key, value
            self.manage[address] = []
            # datas
            self.manage[address].append(message)
            # ACTA time
            self.manage[address].append(time())
            # position on starting block 1 player => car0 => 0
            self.manage[address].append(position)

    def delete_disconnected_player(self):
        connected_players = []
        for addr, val in self.manage.items():
            if time() - val[1] > 1:
                del self.manage[addr]
                print "Deleted in manage dictionnary, and I kill the player: ", addr
            else:
                try:
                    connected_players.append(val[0][13])
                except:
                    connected_players.append("Pb in delete_disconnected_player")
        return connected_players

    def create_msg_cars(self):
        self.msg = osc.Message("/cs")
        for key, value in self.manage.items():
            self.msg.add(key[0])
            for item in value[0]:
                self.msg.add(item)
            # Add position
            self.msg.add(value[2])
        return self.msg

    def create_msg_classement(self):
        self.msg = osc.Message("/ct")
        for key, val in self.manage.items():
            self.msg.add(val[0][13]) # name
            self.msg.add(val[0][12]) # time
        return self.msg

    def reset_data(self):
        self.manage = {}
        self.ACTA = {}
        print "Reset manage and ACTA ..."

if __name__ == "__main__":
    # only to test
    # set instance of class
    game = GameManagement()

    # only to test this script
    test = [
            [('10.0.0.7', 47582), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 0, "toto"]],
            [('10.0.0.5', 41258), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 0, "totu"]],
            [('10.0.0.1', 65872), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 0, "toti"]],

            [('10.0.0.7', 47582), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 0, "toto"]],
            [('10.0.0.5', 41258), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 200, "totu"]],
            [('10.0.0.1', 65872), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 0, "toti"]],

            [('10.0.0.7', 47582), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 0, "toto"]],
            [('10.0.0.5', 41258), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 200, "totu"]],
            [('10.0.0.1', 65872), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 0, "toti"]],

            [('10.0.0.7', 47582), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 0, "toto"]],
            [('10.0.0.5', 41258), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 200, "totu"]],
            [('10.0.0.1', 65872), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 300, "toti"]],

            [('10.0.0.7', 47582), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 0, "toto"]],
            [('10.0.0.5', 41258), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 200, "totu"]],
            [('10.0.0.1', 65872), [3.6, 0.0, 9.5, 0.0, 4.5, 1.3, 300, "toti"]],
            ]

    for t in test:
        sleep(1)
        game.cars_to_dict(t[1], t[0]) # message, address
        print game.manage

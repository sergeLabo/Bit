#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

## bitServer.py

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

#from __future__ import unicode_literals
import os
import sys
import threading
from time import sleep

try:
    from twisted.internet import reactor
except:
    print "You must install python-twisted: http://twistedmatrix.com"

from txosc import async, dispatch, osc
from bitManagement import GameManagement
from wikikIRC_game import MyBot
from etherpad_diff import EtherPad


class UDPSender(object):
    ''' Send datas to Blender with UDP. '''
    def __init__(self, port, host):
        self.port = port
        self.host = host
        self.client = async.DatagramClientProtocol()
        self._client_port = reactor.listenUDP(0, self.client)
        print("Sending on: %s : %s" % (self.host, self.port))

    def send_message(self, message):
        self.client.send(message, (self.host, self.port))


class UDPReceiverApplication(object):
    def __init__(self, port):
        self.port = port
        self.receiver = dispatch.Receiver()
        self._server_port = reactor.listenUDP(self.port,
                                async.DatagramServerProtocol(self.receiver))
        print("Listening on osc.udp://localhost:%s" % (self.port))
        # handler
        #self.receiver.addCallback("/c", servermain.car_handler)


class ServerMain(GameManagement):
    def __init__(self, port_in, port_out,host):
        self.port_in = port_in
        self.port_out = port_out
        self.host = host
        #GameManagement.__init__(self)
        self.pad = [""]

    def game_server(self):
        # Twisted instance with txosc
        self.multicast_sender = UDPSender(self.port_out, self.host)
        self.UDP_receiver = UDPReceiverApplication(self.port_in)
        reactor.run()

    def send2blender(self):
        ''' Send frequency must be less than 60 Hz,
            FPS in Blender is less than 60.
        '''
        while True:
            sleep(0.015)
            # Create bundle with all messages
            bund = self.create_bundle()
            # Send
            self.multicast_sender.send_message(bund)

    def create_bundle(self):
        bund = osc.Bundle()

        # WikikIRC message
        msg_irc = osc.Message("/irc")
        out = mybot.out
        msg_irc.add(out)
        bund.add(msg_irc)

        ### Pad message
        ##msg_pad = osc.Message("/pad")
        ##pad = my_pad.get_new_line()
        ##if my_pad.loopnum < 2:
            ##pad = [""]
        ##line = ''
        ##for l in pad:
            ##line += l
        ##if len(line) > 1:
            ##print line
        ##try:
            ##line = line.encode('utf-8')
        ##except:
            ##pass
        ##msg_pad.add(line)
        ##bund.add(msg_pad)

        return bund


def reinit_message(msg, value):
    # Reinit message after sending
    msg_reinit = osc.Message(msg)
    msg_reinit.add(value)
    return msg_reinit

def clear():
    if (os.name == 'nt'):
        os.system('cls')
    else:
        os.system('clear')

def thread_keyboard():
    hlp = '''
        q + Enter       Quit
        c + Enter       Refresh this terminal'''

    while True:
        clear()
        print hlp
        key = sys.stdin.read(1)
        if key == 'q':
            print("Exit")
            os._exit(0)
        elif key == 'c':
            print("Clear terminal")
        # ignore newlines
        elif key == '\n':
            pass
        else:
            # print help message when no valid command is issued
            print hlp

if __name__ == "__main__":
    host = '127.0.0.1'
    port_out = 8000
    port_in  = 9000

    server_list = [("irc.wikimedia.org", 6667)]
    nickname = "Labomedia-test"
    realname = "Syntaxis analysis in Python with bot"
    address = "http://etherpad.pingbase.net/ServietteFarcie"

    servermain = ServerMain(port_in, port_out, host)

    # Wait on keyboard input
    thread1 = threading.Thread(target=thread_keyboard)
    thread1.start()

    # Serviette farcie
    my_pad = EtherPad(address)

    # Send bundles
    thread2 = threading.Thread(target=servermain.send2blender)
    thread2.start()

    # Bot Wikipedia
    mybot = MyBot(server_list, nickname, realname)
    thread3 = threading.Thread(target=mybot.start)
    thread3.start()

    # Run server
    print "The server is running ..."
    servermain.game_server()

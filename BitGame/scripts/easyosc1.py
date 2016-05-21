#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## easyosc.py

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

from time import time, sleep
import socket
from scripts.OSC import decodeOSC, OSCClient, OSCMessage


class GetOsc():
    ''' Get and Decode OSC messages with UDP Unicast. '''
    def __init__(self, ip="127.0.0.1", port=8000,
                                            buffer_size=1024, timeout=0.01):
        '''
            buffer_size set UDP buffer
            recv(self.buffer_size) empty the buffer every frame
            timeout must be compared to the duration of the frame = 0.016
        '''
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.timeout = timeout
        self.collect_nbr = 0
        self.failed = 0
        self.ratio = 1

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.ip, self.port))
            self.sock.setblocking(0)
            self.sock.settimeout(self.timeout)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,
                                                            self.buffer_size)
            print("Get OSC data on :")
            print("IP = {} : Port = {}  with Buffer = {}".format(self.ip,
                                                self.port, self.buffer_size))
            print()
        except:
            print("No connexion on IP={} Port={}".format(self.ip, self.port))

    def receive(self):
        ''' Return received data. '''
        data = []
        try:
            self.collect_nbr += 1
            raw_data = self.sock.recv(self.buffer_size)
            data = decodeOSC(raw_data)
        except socket.error:
            self.failed += 1
            if time()%2 < 0.01:
                print("No data in receive() in GetOSC")
        if self.collect_nbr == 120:
            self.receiving_ratio()
        return data

    def receiving_ratio(self):
        '''
            Print receipt ratio.
            Sometimes the socket doesn't get data.
        '''

        self.ratio = (self.collect_nbr - self.failed)/self.collect_nbr
        self.failed = 0
        self.collect_nbr = 0
        #print('Receipt ratio = {0:.2f}'.format(self.ratio))


class GetMulticastOsc():
    ''' Get and Decode OSC messages with UDP Multicast. '''
    def __init__(self, ip, port, buffer_size=1024, timeout=0.01):
        '''
            buffer_size set UDP buffer
            BUG:
                recv(self.buffer_size) should empty the buffer every frame
                but this doesn't work.
                In this example, pure data send only every 0.02s.
            timeout must be compared to the duration of the frame = 0.016.
        '''
        self.ANY = "0.0.0.0"
        self.MCAST_ADDR = ip
        self.MCAST_PORT = port
        self.buffer_size = buffer_size
        self.timeout = timeout
        self.collect_nbr = 0
        self.failed = 0
        self.ratio = 1

        try:
            #create a UDP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                                        socket.IPPROTO_UDP)
            #allow multiple sockets to use the same PORT number
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #Bind to the port that we know will receive multicast data
            self.sock.bind((self.ANY, self.MCAST_PORT))
            #tell the kernel that we are a multicast socket
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL,
                                                                        255)
            #Tell the kernel that we want to add ourselves to a multicast group
            #The address for the multicast group is the third param
            status = self.sock.setsockopt(socket.IPPROTO_IP,
                                            socket.IP_ADD_MEMBERSHIP,
                                            socket.inet_aton(self.MCAST_ADDR) \
                                            + socket.inet_aton(self.ANY))
            self.sock.setblocking(0)
            # TODO: BUG
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,
                                                                buffer_size)
            print("Get OSC data on :")
            print("IP = {} : Port = {}  with Buffer = {}".format( \
                        self.MCAST_ADDR, self.MCAST_PORT, self.buffer_size))
            print()
        except:
            print("No connexion on IP={} Port={}".format( \
                                            self.MCAST_ADDR, self.MCAST_PORT))

    def receive(self):
        ''' Return received data. '''
        data = []
        try:
            self.collect_nbr += 1
            raw_data = self.sock.recv(self.buffer_size)
            data = decodeOSC(raw_data)
            #print("data =", data)
        except socket.error:
            self.failed += 1
            if time()%2 < 0.01:
                print("No data in receive() in GetOSC")
        if self.collect_nbr == 120:
            self.receiving_ratio()
        return data

    def receiving_ratio(self):
        '''
            Print receipt ratio.
            Sometimes the socket doesn't get data.
        '''

        self.ratio = (self.collect_nbr - self.failed)/self.collect_nbr
        self.failed = 0
        self.collect_nbr = 0
        print('Ratio de réception dans get_osc.py= {0:.2f}'.format(self.ratio))


class SendOsc(OSCClient):
    ''' Send OSC messages. '''

    def __init__(self, verbose):
        ''' Socket creation. '''
        OSCClient.__init__(self, server=None)
        self.verbose = verbose
        
    def send_simple_message(self, address, title, message):
        ''' address = tuple ip, port
            title = '/some_stuff'
            message is one int or float or str, only one
        '''

        msg = OSCMessage(title)
        msg.append(message)
        try:
            OSCClient.sendto(self, msg, address)
        except:
            if self.verbose:
                print("Send problem on {}".format(address))


    def send_messages_in_list(self, address, title, messages_in_list):
        ''' address = tuple ip, port
            title = '/some_stuff'
            messages_in_list = list of str or int or float

        '''
        msg = OSCMessage(title)
        for m in messages_in_list:
            msg.append(m)
        try:
            OSCClient.sendto(self, msg, address)
        except:
            #print("Send problem on {}".format(address))
            pass


if __name__ == "__main__":
    def test0():
        getOPY = GetOsc("192.168.1.4", 9000, 1024)
        sendOPY = SendOsc()

        a = 0
        while True:
            sleep(0.15)
            sendOPY.send_simple_message(("192.168.1.4", 9000), '/blender/x', 5)

    def test2():
        getOPY = GetMulticastOsc("224.0.0.11", 28888, 1024)
        while True:
            sleep(0.15)
            data = getOPY.receive()
            print(data)

    #test0()
    #text2()



#!/usr/bin/python2.7
# -*- coding: utf8 -*-

# etherpad_API.py

from py_etherpad import EtherpadLiteClient

myPad = EtherpadLiteClient(None, 'http://etherpad.pingbase.net/ServietteFarcie')

#Change the text of the etherpad
t = myPad.getText()

print "ok"

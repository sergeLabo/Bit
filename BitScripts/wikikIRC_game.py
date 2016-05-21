#!/usr/bin/python2.7
# -*- coding: utf8 -*-

## wikikIRC_game.py

# WikikIRC by Olivier Baudu, Anthony Templier for Labomedia September 2011.
# Modified by Sylvain Blocquaux 2012.
# Modified for Le Bit de Dieu by SergeBlender for Labomedia November 2013.
# olivier arobase labomedia point net // http://lamomedia.net
# Published under License GPLv3: http://www.gnu.org/licenses/gpl-3.0.html

#from __future__ import unicode_literals
import re
import urllib2
from bs4 import BeautifulSoup
from irc.bot import SingleServerIRCBot

black_list   = ['<ref>', '</ref>',
                '<br>',
                '<!-- BEGIN BOT SECTION -->',
                'listeRecents', 'BEGIN BOT SECTION', 'DEFAULTSORT',
                'BASEPAGENAME', 'TOC',
                'noinclude', 'small', 'align', 'left', 'right', 'center',
                'includeonly', '#switch',
                '{pt}', '{cons}', 'thumb', 'clr', 'nbsp', 'Infobox',
                '::', ':::',  '::::', '::::', '::::',
                 '^', '~', '--', '<', '>', '[', ']', '{', '}', '/', '*',
                 '=', '|', '\'']


class MyBot(SingleServerIRCBot):
    def __init__(self, server_list, nickname, realname):
        SingleServerIRCBot.__init__(self, server_list, nickname, realname)
        self.out = ''

    def on_welcome(self, serv, ev):
        # IRC connection
        print ("\n Connexion on IRC...\n")
        serv.join("#fr.wikipedia")

    def on_pubmsg(self, serv, ev):
        # Get new message
        message = ev.arguments[0]
        # Delete color codes codes and get only text
        messageIRC = re.compile("\x03[0-9]{0,2}").sub('', message)

        addressPosition = re.search("http://fr.wikipedia.org", messageIRC)
        if addressPosition != None :
            address = messageIRC[addressPosition.start(0):]
            tab = re.split('&', address)
            address = tab[0]

            # Get wikipedia modif page
            req = urllib2.Request(address)
            # Add header becauce wikipedia expected a navigator
            req.add_header('User-agent', 'WikikIRC-0.4')
            # Read diff wikipedia page
            fp = urllib2.urlopen(req)
            text = fp.read()
            #print("text", type(text))
            # text = <type 'str'>

            fp.close()

            # text = str = encode in 2.7, I decode
            html = text.decode('UTF-8')
            #print("html", type(html))
            # <type 'unicode'>

            # Return a list with item = lines, lines are finished with \n
            lines = html.splitlines()
            a = 0
            for line in lines:
                if '<td class="diff-context"><div>' in line :
                    a += 1
                    if a == 1:
                        soup = BeautifulSoup(line)
                        out = soup.get_text()
                        # out <type 'unicode'>, u"
                        out = out.encode('UTF-8')
                        for i in ['style', 'class="' ]:
                            if i in out:
                                out = ' '
                        # Cleaning
                        for i in black_list:
                            out = out.replace(i, ' ')
                        # Delete added space
                        for i in ['    ', '   ', '  ']:
                            out = out.replace(i, ' ')
                        # Delete beginning space
                        if out[0] in [' ', ':', ';', '!']:
                            out = out[1:]
                        if len(out) > 20:
                            self.out = out

if __name__ == "__main__":
    server_list = [("irc.wikimedia.org", 6667)]
    nickname = "Labomedia-test"
    realname = "Syntaxis analysis in Python with bot"

    MyBot(server_list, nickname, realname).start()

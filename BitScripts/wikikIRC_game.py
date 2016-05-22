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
        print("Message brut:\n", message)
        # Delete color codes codes and get only text
        messageIRC = re.compile("\x03[0-9]{0,2}").sub('', message)

        addressPosition = re.search("https://fr.wikipedia.org", messageIRC)

        out = None
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
            #print("text", text)
            fp.close()

            # text = str = encode in 2.7, I decode
            html = text.decode('UTF-8')
            #print("html", html)

            # Return a list with item = lines, lines are finished with \n
            lines = html.splitlines()
            a = 0
            for line in lines:
                if '<td class="diff-context"><div>' in line :
                    a += 1
                    if a == 1:
                        soup = BeautifulSoup(line, "html5lib")
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
        print("Message propre:\n", out)



if __name__ == "__main__":
    server_list = [("irc.wikimedia.org", 6667)]
    nickname = "Labomedia-test"
    realname = "Syntaxis analysis in Python with bot"

    MyBot(server_list, nickname, realname).start()

'''

/usr/lib/python2.7/site-packages/bs4/__init__.py:166: UserWarning: No parser was explicitly specified, so I'm using the best available HTML parser for this system ("html5lib"). This usually isn't a problem, but if you run this code on another system, or in a different virtual environment, it may use a different parser and behave differently.

To get rid of this warning, change this:

 BeautifulSoup([your markup])

to this:

 BeautifulSoup([your markup], "html5lib")

  markup_type=markup_type))

'''

#!/usr/bin/python3
# -*- coding: UTF-8 -*-

## wikikIRC_game.py

# WikikIRC by Olivier Baudu, Anthony Templier for Labomedia September 2011.
# Modified by Sylvain Blocquaux 2012.
# Modified for Le Bit de Dieu by SergeBlender for Labomedia November 2013.
# olivier arobase labomedia point net // http://lamomedia.net
# Published under License GPLv3: http://www.gnu.org/licenses/gpl-3.0.html

import re
import urllib.request as request
from bs4 import BeautifulSoup
from irc.bot import SingleServerIRCBot


black_list   = ['< ref>', '<', '>', '<br>', '<>', '&nbsp', '^', '~', '--',
                '__NOINDEX__', 'class "wikitable sortable"', 'noinclude',
                'class "wikitable"', 'sup_entête2', 'align "center"',
                'align "left"', 'colspan',
                '::', ':::', '[', ']', '{', '}', '/', '*', '=', '|', '\'']


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
            #print(address)
            req = request.Request(address)
            # Add header becauce wikipedia expected a navigator
            req.add_header('User-agent', 'WikikIRC-0.4')

            # Read diff wikipedia page
            fp = request.urlopen(req)
            text = fp.read()
            fp.close()
            html = text.decode(encoding='UTF-8')

            # Return a list with item = lines, lines are finished with \n
            lines = html.splitlines()
            a = 0
            for line in lines:
                if '<td class="diff-context"><div>' in line :
                    a += 1
                    if a ==1:
                        soup = BeautifulSoup(line)
                        out = soup.get_text()
                        # Cleaning
                        for i in black_list:
                            out = out.replace(i, ' ')
                        pattern = '#/d/d/d/d/d/d'
                        out = re.sub(pattern, ' ', out)
                        # Delete added space
                        for i in ['    ', '   ', '  ']:
                            out = out.replace(i, ' ')
                        # Delete beginning space
                        if out[0] == ' ':
                            out = out[1:]
                        if len(out) > 2:
                            print(out, '\n')
                            self.out = out


if __name__ == "__main__":
    server_list = [("irc.wikimedia.org", 6667)]
    nickname = "Labomedia-test"
    realname = "Syntaxis analysis in Python with bot"

    MyBot(server_list, nickname, realname).start()

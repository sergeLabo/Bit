#!/usr/bin/python2.7
# -*- coding: utf8 -*-

# etherpad_diff.py

#############################################################################
# Copyright (C) Labomedia June 2013
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


from time import sleep
import urllib2
import re
from bs4 import BeautifulSoup

class EtherPad():
    def __init__(self, address):
        ''' address de l'etherpad '''
        self.address = address
        self.newlines = [''] # list
        self.oldlines = ['rien du tout'] # list of str
        self.dejavulines = ['toujours rien'] # list of str
        self.loopnum = 0
        self.nb_line = 0

    def toutes_les_nouvelles_lignes(self, pagediff):
        '''Retourne seulement les nouvelles lignes dans une liste.'''
        jamaisvu, poemlines = [""], [""]
        for line in pagediff:
            # var clientVars est le début de la bonne ligne
            if "var clientVars" in line:
                # ce que je cherche est entre: text et attribs
                result = re.search('text(.*)attribs', line)
                # je coupe 3 gri gri avant et à la fin
                poem = result.group(1)[3:-3]
                # je crée les lignes
                poem = poem.replace('\\n', "\\\n")
                poemlines = poem.splitlines()
                # je supprime le déjà vu
                jamaisvu = list(set(poemlines) - set(self.dejavulines))
        # Sauvegarde par défaut de toutes les nouvelles lignes
        self.dejavulines = poemlines

        return jamaisvu, poemlines


    # def nb_lignes(self, jamaisvu, poemlines):
        # self.nb_line

    def lignes_finies(self, jamaisvu, poemlines):
        ''' Avec toutes les nouvelles lignes,
            retourne les lignes avec end line.
            Sauvegarde les lignes vues.
        '''
        # Liste par défaut des lignes à afficher
        lignes_finies = [""]
        # si jamaisvu n'est pas une liste vide
        if jamaisvu != []:
            # Si la ligne n'est pas finie
            if re.search(repr('\\n'), jamaisvu[-1]):
                # Je supprime la dernière ligne
                lignes_finies = jamaisvu[:1]
                # Je supprime la ligne dans la sauvegarde du poem
                self.dejavulines.remove(jamaisvu[-1])
                print("je ne passe jamais par là !")
            # Sinon, je garde tout
            else:
                lignes_finies = jamaisvu

        # Suppression des \ à la fin de chaque ligne
        if len(lignes_finies) >0:
            for i in range(len(lignes_finies)):
                if lignes_finies[i] == "\\":
                    lignes_finies[i] = lignes_finies[i][:-1]
        return lignes_finies

    def get_new_line(self):
        self.loopnum += 1
        # Request
        text = "Le bit ou le néant !"
        try:
            req = urllib2.Request(self.address)
            fp = urllib2.urlopen(req)
            text = fp.read()
            fp.close()
        except:
            print("Problème de connexion")
        lines = soup_extraction(text)

        # 1er filtre
        pagediff = list(set(lines) - set(self.oldlines))
        # Sauvegarde
        self.oldlines = lines

        # 2ème filtre: je trouve toutes les lignes
        jamaisvu, poemlines = self.toutes_les_nouvelles_lignes(pagediff)

        # 3ème filtre: je ne garde que les lignes avec end line
        self.newlines = self.lignes_finies(jamaisvu, poemlines)

        return self.newlines

    def jaffiche(self, lines):
        if self.loopnum > 1:
            for l in lines:
                print(l)
            print

def soup_extraction(text):
    ''' Extraction de la soupe, retourne list de lignes.'''
    html = text.decode('UTF-8')
    soup = BeautifulSoup(html, "html5lib")
    prettisoup = soup.prettify()
    lines = prettisoup.splitlines()
    return lines


if __name__ == "__main__":
    address = "http://etherpad.pingbase.net/ServietteFarcie"
    my_pad = EtherPad(address)
    doloop = True
    while doloop:
        jamaisvu = my_pad.get_new_line()
        my_pad.jaffiche(jamaisvu)
        sleep(2)

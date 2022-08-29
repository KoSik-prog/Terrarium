#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        settings
#              read / write settings
#
# Author:      KoSik
#
# Created:     28.08.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
import xml.etree.cElementTree as ET

from libraries.log import *
from terrarium import *

class settings_CL:
    #def __init__(self):

    def zapis_ustawien_xml(self):
        setings = ET.Element("settings")

        ET.SubElement(setings, "minWilgotnosc").text = str(terrarium.minWilgotnosc)

        tree2 = ET.ElementTree(setings)
        tree2.write('Desktop/terra/ustawienia.xml')
        log.add_log("Zapisano ustawienia")

    def odczyt_ustawien_xml(self):
        tree = ET.ElementTree(file='Desktop/terra/ustawienia.xml')
        root = tree.getroot()

        terrarium.minWilgotnosc = int(root.find('minWilgotnosc').text)
        log.add_log("Odczytano ustawienia")

settings = settings_CL()
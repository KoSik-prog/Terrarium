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
    def __init__(self, filePath):
        self.filePath + = filePath

    def zapis_ustawien_xml(self):
        setings = ET.Element("settings")

        ET.SubElement(setings, "minWilgotnosc").text = str(terrarium.minWilgotnosc)

        tree2 = ET.ElementTree(setings)
        tree2.write(self.filePath + 'ustawienia.xml')
        log.add_log("Settings saved")

    def odczyt_ustawien_xml(self):
        tree = ET.ElementTree(file= self.filePath + 'ustawienia.xml')
        root = tree.getroot()

        terrarium.minWilgotnosc = int(root.find('minWilgotnosc').text)
        log.add_log("Settings loaded")

settings = settings_CL('Desktop/terra/')
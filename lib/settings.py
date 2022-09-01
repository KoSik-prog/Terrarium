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

from lib.log import *
from terrarium import *

class Settings:
    def __init__(self, filePath):
        self.filePath = filePath

    def save_settings(self):
        setings = ET.Element("settings")

        ET.SubElement(setings, "minHumidity").text = str(terrarium.minimumHumidity)

        tree2 = ET.ElementTree(setings)
        tree2.write(self.filePath + 'settings.xml')
        log.add_log("Settings saved")

    def load_settings(self):
        tree = ET.ElementTree(file= self.filePath + 'settings.xml')
        root = tree.getroot()

        terrarium.minimumHumidity = int(root.find('minHumidity').text)
        log.add_log("Settings loaded")

settings = Settings('Desktop/terra/')
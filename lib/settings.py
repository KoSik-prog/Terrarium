#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        settings
#              read / write settings
#
# Author:      KoSik
#
# Created:     28.08.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import xml.etree.cElementTree as ET
    from timeit import default_timer as tim
    import datetime
    from lib.heater import *
    from lib.sprayer import *
    from lib.log import *
    from terrarium import *
except ImportError:
    print("Import error - settings")


class Settings:
    def __init__(self, filePath):
        self.filePath = filePath

    def save_settings(self):
        setings = ET.Element("settings")

        ET.SubElement(setings, "minHumidity").text = str(
            terrarium.minimumHumidity)
        ET.SubElement(setings, "sprying1").text = str(sprayer.spraying1)
        ET.SubElement(setings, "sprying2").text = str(sprayer.spraying2)
        ET.SubElement(setings, "sprayingTime").text = str(sprayer.sprayingTime)
        ET.SubElement(setings, "sprayingTimeManual").text = str(
            sprayer.sprayingTimeManual)
        ET.SubElement(setings, "minimumHumidity").text = str(
            terrarium.minimumHumidity)
        ET.SubElement(setings, "temperatureRequiredIsland").text = str(
            terrarium.temperatureRequiredIsland)
        ET.SubElement(setings, "minUviForHeating").text = str(
            terrarium.minUviForHeating)

        tree2 = ET.ElementTree(setings)
        tree2.write(self.filePath + 'settings.xml')
        log.add_log("Settings saved")

    def load_settings(self):
        tree = ET.ElementTree(file=self.filePath + 'settings.xml')
        root = tree.getroot()

        terrarium.minimumHumidity = int(root.find('minHumidity').text)
        sprayer.spraying1 = datetime.datetime.strptime(
            root.find('sprying1').text, '%H:%M:%S').time()
        sprayer.spraying2 = datetime.datetime.strptime(
            root.find('sprying2').text, '%H:%M:%S').time()
        sprayer.sprayingTime = int(root.find('sprayingTime').text)
        sprayer.sprayingTimeManual = int(root.find('sprayingTimeManual').text)
        terrarium.minimumHumidity = int(root.find('minimumHumidity').text)
        terrarium.temperatureRequiredIsland = float(
            root.find('temperatureRequiredIsland').text)
        terrarium.minUviForHeating = float(root.find('minUviForHeating').text)

        log.add_log("Settings loaded")


settings = Settings('Desktop/terra/')

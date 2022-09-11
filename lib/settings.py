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
    from terrarium import *
    from lib.heater import *
    from lib.sprayer import *
    from lib.log import *
    from lib.mainLight import *
except ImportError:
    print("Import error - settings")


class Settings:
    def __init__(self, filePath):
        self.filePath = filePath

    def save_settings(self):
        setings = ET.Element("settings")
        
        ET.SubElement(setings, "sprying1").text = str(sprayer.get_spraying_timer(0))
        ET.SubElement(setings, "sprying2").text = str(sprayer.get_spraying_timer(1))
        ET.SubElement(setings, "sprayingTime").text = str(sprayer.get_spraying_time())
        ET.SubElement(setings, "sprayingTimeManual").text = str(sprayer.get_spraying_time_manual())
        ET.SubElement(setings, "minimumHumidity").text = str(terrarium.get_minimum_humidity())
        ET.SubElement(setings, "temperatureRequiredIsland").text = str(terrarium.get_requred_island_temperature())
        ET.SubElement(setings, "minUviForHeating").text = str(terrarium.get_min_uvi_for_heating())
        ET.SubElement(setings, "mainLightOnTime").text = str(mainLight.get_timer_str(0))
        ET.SubElement(setings, "mainLightOffTime").text = str(mainLight.get_timer_str(1))

        tree2 = ET.ElementTree(setings)
        tree2.write(self.filePath + 'settings.xml')
        log.add_log("Settings saved")

    def load_settings(self):
        tree = ET.ElementTree(file=self.filePath + 'settings.xml')
        root = tree.getroot()
        
        sprayer.set_spraying_timer(0, datetime.datetime.strptime(root.find('sprying1').text, '%H:%M:%S').time())
        sprayer.set_spraying_timer(1, datetime.datetime.strptime(root.find('sprying2').text, '%H:%M:%S').time())
        sprayer.set_spraying_time(int(root.find('sprayingTime').text))
        sprayer.set_spraying_time_manual(int(root.find('sprayingTimeManual').text))
        terrarium.set_minimum_humidity(int(root.find('minimumHumidity').text))
        terrarium.set_requred_island_temperature(float(root.find('temperatureRequiredIsland').text))
        terrarium.set_min_uvi_for_heating(float(root.find('minUviForHeating').text))
        mainLight.set_timer(0, root.find('mainLightOnTime').text)
        mainLight.set_timer(1, root.find('mainLightOffTime').text)

        log.add_log("Settings loaded")


settings = Settings('Desktop/terra/')

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        terrarium main program
# Purpose:
#
# Author:      KoSik
#
# Created:     06.08.2020
# Copyright:   (c) kosik 2020
#-------------------------------------------------------------------------------
import pygame, pygame.mixer, pygame.gfxdraw, glob, time, sys, datetime, smbus, board, busio, adafruit_veml6075, threading, os, timeit
from pygame.locals import *
from pygame.compat import unichr_, unicode_
from pygame.locals import *
from pygame.compat import geterror
import xml.etree.cElementTree as ET

from timeit import default_timer as timer

from libraries.log import *
from libraries.mainLight import *
from libraries.sensors import *
from libraries.heater import *
from libraries.sprayer import *
from libraries.display import *
from libraries.gui import *
from libraries.communication import *
from terrarium import *
#+++++++++++++++++++++ delay for safety +++++++++++++++++++++++++++
time.sleep(10)
######################################################################################
def zapis_ustawien_xml():
    setings = ET.Element("settings")

    ET.SubElement(setings, "minWilgotnosc").text = str(terrarium.minWilgotnosc)

    tree2 = ET.ElementTree(setings)
    tree2.write('Desktop/terra/ustawienia.xml')
    log.add_log("Zapisano ustawienia")

def odczyt_ustawien_xml():
    tree = ET.ElementTree(file='Desktop/terra/ustawienia.xml')
    root = tree.getroot()

    terrarium.minWilgotnosc = int(root.find('minWilgotnosc').text)
#++++++++++++++++ THREADS DEFINITIONS ++++++++++++++++++++++++++++++++++++++++++++++++++
def thread_sensors_init():
    sensorsTH = threading.Thread(target = sensors.sensors_thread)
    sensorsTH.start()

def thread_main_light_init():
    mainLightTH = threading.Thread(target = mainLight.main_light_thread)
    mainLightTH.start()

def thread_heater_init():
    heaterTH = threading.Thread(target = heater.heater_thread)
    heaterTH.start()

def thread_heater_pwm_control_init():
    heaterPwmControlTH = threading.Thread(target = heater.pwm_control_thread)
    heaterPwmControlTH.start()

def thread_sprayer_init():
    sprayerTH = threading.Thread(target = sprayer.sprayer_thread)
    sprayerTH.start()

def thread_gui_init():
    guiTH = threading.Thread(target = gui.gui_thread)
    guiTH.start()

def thread_touch_init():
    touchTH = threading.Thread(target = gui.touch_thread)
    touchTH.start()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#-----START-------------------------------------------------------------------------------------------------------------------------------------------
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():
    log.add_log("Starting...")

    zapis_ustawien_xml()
    odczyt_ustawien_xml()
    #-------------THREADS INIT--------------------------------
    thread_sensors_init()
    thread_main_light_init()
    thread_heater_init()
    thread_heater_pwm_control_init()
    thread_sprayer_init()
    thread_gui_init()
    thread_touch_init()
    #--------------MAIN FUNCTION------------------------------
    while(1):
        #---------------WYSYLANIE-----------------------------
        socket.send_message_to_server()
        time.sleep(1)
    pass

if __name__ == '__main__':
    main()

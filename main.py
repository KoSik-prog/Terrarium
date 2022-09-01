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
import glob, time, sys, datetime, threading, os, timeit

from timeit import default_timer as timer

from lib.log import *
from lib.mainLight import *
from lib.sensors import *
from lib.heater import *
from lib.sprayer import *
from lib.display import *
from lib.gui import *
from lib.communication import *
from lib.settings import *
from lib.watchdog import *
from terrarium import *
#+++++++++++++++++++++ delay for safety +++++++++++++++++++++++++++
time.sleep(10)
######################################################################################

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
    lastWatchdogResetTime = datetime.datetime.now()

    log.add_log("Starting...")
    settings.save_settings()
    settings.load_settings()
    #-------------THREADS INIT--------------------------------
    thread_sensors_init()
    thread_main_light_init()
    thread_heater_init()
    thread_sprayer_init()
    thread_gui_init()
    thread_touch_init()
    #--------------MAIN FUNCTION------------------------------
    while(1):
        #---------------WYSYLANIE-----------------------------
        socket.send_message_to_server()
        time.sleep(1)
        
        duration = datetime.datetime.now() - lastWatchdogResetTime
        if(duration.total_seconds() >= 60): #60 seconds to watchdog flag reset
            watchdog.reset()
            lastWatchdogResetTime = datetime.datetime.now()
    pass

if __name__ == '__main__':
    main()

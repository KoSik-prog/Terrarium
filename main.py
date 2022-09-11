#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        terrarium main program
# Purpose:
#
# Author:      KoSik
#
# Created:     06.08.2020
# Copyright:   (c) kosik 2020
# -------------------------------------------------------------------------------
try:
    import glob
    import time
    import sys
    import datetime
    import os
    import threading
    from terrarium import *
    from timeit import default_timer as timer
    from lib.log import *
    from lib.communication import *
    from lib.mainLight import *
    from lib.sensors import *
    from lib.heater import *
    from lib.sprayer import *
    from lib.gui import *
    from lib.watchdog import *
    from lib.fogger import *
except ImportError:
    print("Import error - terrarium main program")


class Main:
    sensorsLastUpdateTime = 0
    mainLightLastUpdateTime = 0
    heaterLastUpdateTime = 0
    lastWatchdogResetTime = datetime.datetime.now()

    def __init__(self):
        log.add_log("Starting...")
        # +++++++++++++++++++++ delay for safety ++++++++++++++++++
        time.sleep(10)
        ###########################################################
        #settings.save_settings()
        settings.load_settings()
        # -------------THREADS INIT--------------------------------
        self.thread_sensors_init()
        self.thread_main_light_init()
        self.thread_heater_init()
        self.thread_sprayer_init()
        self.thread_gui_init()
        self.thread_touch_init()
        # --------------MAIN FUNCTION------------------------------
        self.start_terra()

    def start_terra(self):
        while terrarium.runFlag == True:
            socket.send_message_to_server()
            time.sleep(1)

            duration = datetime.datetime.now() - self.lastWatchdogResetTime
            if (duration.total_seconds() >= 60):  # 60 seconds to watchdog flag reset
                watchdog.reset()
                self.lastWatchdogResetTime = datetime.datetime.now()

    def thread_sensors_init(self):
        sensorsTH = threading.Thread(target=sensors.sensors_thread)
        sensorsTH.start()

    def thread_main_light_init(self):
        mainLightTH = threading.Thread(target=mainLight.main_light_thread)
        mainLightTH.start()

    def thread_heater_init(self):
        heaterTH = threading.Thread(target=heater.heater_thread)
        heaterTH.start()

    def thread_sprayer_init(self):
        sprayerTH = threading.Thread(target=sprayer.sprayer_thread)
        sprayerTH.start()

    def thread_gui_init(self):
        guiTH = threading.Thread(target=gui.gui_thread)
        guiTH.start()

    def thread_touch_init(self):
        touchTH = threading.Thread(target=gui.touch_thread)
        touchTH.start()


# -----START-------------------------------------
if __name__ == "__main__":
    main = Main()

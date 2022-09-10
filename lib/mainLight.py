#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        mainLight
# Purpose:
#
# Author:      KoSik
#
# Created:     26.08.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import datetime
    from timeit import default_timer as timer
    from terrarium import *
    from lib.inout import *
    from lib.log import *
    from lib.heater import *
except ImportError:
    print("Import error - displayBrightness")


class MainLight:
    manualControlFlag = False
    timeToResume = 20  # seconds - time until the lamp is turned on after restarting

    def __init__(self, pin, autoOn, autoOff):
        gpio.set_as_output(pin)
        self.pin = pin
        self.autoOn = autoOn
        self.autoOff = autoOff

    def main_light_thread(self):
        while terrarium.runFlag == True:
            self.check_timer()
            terrarium.mainLightLastUpdateTime = datetime.datetime.now()
            time.sleep(10)

    def check_timer(self):
        format = '%H:%M:%S.%f'
        actualTime = datetime.datetime.now().time()

        try:
            onTimeDifference = datetime.datetime.strptime(
                str(actualTime), format) - datetime.datetime.strptime(self.autoOn, format)
        except ValueError as e:
            log.add_log('error: ', e)
        try:
            offTimeDifference = datetime.datetime.strptime(
                str(actualTime), format) - datetime.datetime.strptime(self.autoOff, format)
        except ValueError as e:
            log.add_log('error: ', e)
        # ------ clear flags ------------------------
        if (int(onTimeDifference.total_seconds()) > (-15) and int(onTimeDifference.total_seconds()) < 0 and self.manualControlFlag == True):
            self.manualControlFlag = False
        if (int(offTimeDifference.total_seconds()) > (-15) and int(offTimeDifference.total_seconds()) < 0 and self.manualControlFlag == True):
            self.manualControlFlag = False
        # ------ check ------------------------
        end = timer()
        startupTime = datetime.timedelta(seconds=round(end - terrarium.startTime))
        if (gpio.check_main_light_flag() == 0 and (int(onTimeDifference.total_seconds()) > 0) and (int(offTimeDifference.total_seconds()) < (-60)) and self.manualControlFlag == False and startupTime.total_seconds() >= self.timeToResume):
            log.add_log("AUTO main light -> ON")
            gpio.lamp_on(self.pin)
            time.sleep(20)
        if (gpio.check_main_light_flag() == 1 and (int(offTimeDifference.total_seconds()) > 0) and (int(offTimeDifference.total_seconds()) < 60) and self.manualControlFlag == False):
            log.add_log("AUTO main light -> OFF")
            heater.set_heat_control_flag(False)
            heater.dim_light()
            time.sleep(0.5)
            gpio.lamp_off(self.pin)
            time.sleep(20)


mainLight = MainLight(19, '8:00:00.0000', '19:00:00.0000')

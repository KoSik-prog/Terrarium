#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        sprayer
#
# Author:      KoSik
#
# Created:     28.08.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
from timeit import default_timer as tim
from datetime import *
import time as tm

from terrarium import *
from lib.log import *
from lib.inout import *

class Sprayer:
    spraying1 = datetime.time(9, 0)
    spraying2 = datetime.time(17, 00)
    automaticSprayerTimeOn = datetime.time(9, 00) #additional spraying is active during these time
    automaticSprayerTimeOff = datetime.time(17, 00)
    sprayingTime = 12
    sprayingTimeManual = 12
    lastSpraying = 0
    minTimeBetweenSprayings = 300

    def __init__(self, pin):
        gpio.set_as_output(pin)
        self.pin = pin
        self.lastSpraying = tim()

    def sprayer_thread(self):
        while(terrarium.runFlag == True):
            nowStamp = datetime.datetime.now()
            if self.check_time(self.automaticSprayerTimeOn, nowStamp) == True or self.check_time(self.automaticSprayerTimeOff, nowStamp) == True:
                self.spray_terrarium(self.sprayingTime)
                tm.sleep(60)
            #-------------------------------------
            if nowStamp.time() > self.automaticSprayerTimeOn and nowStamp.time() < self.automaticSprayerTimeOff:
                if(terrarium.humidityBottom > 5 and terrarium.humidityBottom < terrarium.minimumHumidity and (tim() - self.lastSpraying) > self.minTimeBetweenSprayings):
                    self.spray_terrarium(self.sprayingTime)
                    tm.sleep(60)
            #------------
            tm.sleep(10)

    def spray_terrarium(self, sprayTime):
        log.add_log('Spraying!')
        gpio.sprayer_on(self.pin)
        tm.sleep(int(sprayTime))
        gpio.sprayer_off(self.pin)
        self.lastSpraying = tim()

    def check_time(self, time1, time2):
        if time1.hour == time2.hour and time1.minute == time2.minute:
            return True
        else:
            return False

sprayer = Sprayer(21)
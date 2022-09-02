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
from timeit import default_timer as timer
import time

from terrarium import *
from lib.log import *
from lib.inout import *

class Sprayer:
    on1H=9
    on1M=0
    on2H=15
    on2M=0
    sprayingTime=12
    sprayingTimeManual = 12
    lastSpraying = 0

    def __init__(self, pin):
        gpio.set_as_output(pin)
        self.pin = pin
        self.lastSpraying = timer()

    def sprayer_thread(self):
        hour1='09'  #additional spraying is active during these hours
        minutes1='18'
        gpio.sprayer_off(self.pin)

        while(terrarium.runFlag == True):
            end = timer()
            timeNow = self.time_now()
            if timeNow == self.format_time(self.on1H, self.on1M):
                print(timeNow)
                if timeNow == self.format_time(self.on2H, self.on2M):
                    self.spray_terrarium(self.sprayingTime)
                    time.sleep(50)
            #-------------------------------------
            teraz = datetime.datetime.now()
            if(int(teraz.hour) >= int(hour1) and int(teraz.hour) <= int(minutes1)):
                if(terrarium.humidityBottom > 5 and terrarium.humidityBottom < terrarium.minimumHumidity and (end - self.lastSpraying)>300):
                    self.spray_terrarium(self.sprayingTime)
                    time.sleep(50)
            #------------
            time.sleep(10)

    def spray_terrarium(self, sprayTime):
        log.add_log('Spraying!')
        gpio.sprayer_on(self.pin)
        time.sleep(int(sprayTime))
        gpio.sprayer_off(self.pin)
        self.lastSpraying = timer()

    def time_now(self):
        nowtime = datetime.datetime.now()
        return self.format_time(nowtime.hour, nowtime.minute)

    def format_time(self, hour, minute):
        return '{:02d}:{:02d}'.format(hour, minute)

sprayer = Sprayer(21)
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
from libraries.log import *
from libraries.inout import *

class sprayerCL:
    on1H=9
    on1M=0
    on2H=15
    on2M=0
    czasSpryskiwania=12
    czasSpryskManual=5
    flaga = False
    ostatnieSpryskanie = 0

    def __init__(self, pin):
        gpio.set_as_output(pin)
        self.pin = pin
        self.ostatnieSpryskanie = timer()

    def sprayer_thread(self):
        czas1='09'  #w tych godzinach aktywne dodatkowe spryskiwanie
        czas2='18'
        gpio.sprayer_off(self.pin)

        while(terrarium.runFlag == True):
            end = timer()
            timeNow = self.time_now()
            if timeNow == self.format_time(self.on1H, self.on1M):
                print(timeNow)
                if timeNow == self.format_time(self.on2H, self.on2M):
                    self.spray_terrarium(self.czasSpryskiwania)
                    time.sleep(50)
            #-------------------------------------
            teraz = datetime.datetime.now()
            if(int(teraz.hour) >= int(czas1) and int(teraz.hour) <= int(czas2)):
                if(terrarium.wilgD > 5 and terrarium.wilgD < terrarium.minWilgotnosc and (end - self.ostatnieSpryskanie)>300):
                    self.spray_terrarium(self.czasSpryskiwania)
                    time.sleep(50)
            #------------
            time.sleep(10)

    def spray_terrarium(self, sprayTime):
        log.add_log('Spraying!')
        self.flaga = True
        gpio.sprayer_on(self.pin)
        time.sleep(int(sprayTime))
        gpio.sprayer_off(self.pin)
        self.flaga = False
        self.ostatnieSpryskanie = timer()

    def time_now(self):
        nowtime = datetime.datetime.now()
        return self.format_time(nowtime.hour, nowtime.minute)

    def format_time(self, hour, minute):
        return '{:02d}:{:02d}'.format(hour, minute)

sprayer = sprayerCL(21)
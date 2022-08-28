#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        mainLight
# Purpose:
#
# Author:      KoSik
#
# Created:     26.08.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
import datetime
import RPi.GPIO as GPIO
from timeit import default_timer as timer

from terrarium import *
from libraries.log import *

class MAIN_LIGHT_CL:
    flag = False
    """AutoON = '8:00:00.0000'
    AutoOFF = '19:15:00.0000'#'19:45:00.0000'"""
    dimmingTime = 12 #czas stopniowego wygaszania w minutach
    manualControlFlag = False
    timeToResume = 30 #seconds - czas do wlaczenia lampy po ponownym uruchomieniu

    def __init__(self, pin, AutoON, AutoOFF):
        GPIO.setup(pin, GPIO.OUT)
        self.pin = pin
        self.AutoON = AutoON
        self.AutoOFF = AutoOFF

    def main_light_thread(self):
        while terrarium.runFlag == True:
            self.check_timer()
            terrarium.mainLightLastUpdateTime = datetime.datetime.now()
            time.sleep(10)

    def check_timer(self):
        format = '%H:%M:%S.%f'
        actualTime=datetime.datetime.now().time()

        try:
            onTimeDifference = datetime.datetime.strptime(str(actualTime), format) - datetime.datetime.strptime(self.AutoON, format)
        except ValueError as e:
            log.add_log('error: ', e)
        try:
            offTimeDifference = datetime.datetime.strptime(str(actualTime), format) - datetime.datetime.strptime(self.AutoOFF, format)
        except ValueError as e:
            log.add_log('error: ', e)
        # clear flags 
        if(int(onTimeDifference.total_seconds())>(-15) and int(onTimeDifference.total_seconds())<0 and  self.manualControlFlag==True):
            self.manualControlFlag=False
        if(int(offTimeDifference.total_seconds())>(-15) and int(offTimeDifference.total_seconds())<0 and self.manualControlFlag==True):
            self.manualControlFlag=False
        #------check------------------------
        end = timer()
        startupTime = datetime.timedelta(seconds=round(end - terrarium.startTime))
        if(self.flag==0 and (int(onTimeDifference.total_seconds())>0) and (int(offTimeDifference.total_seconds())<(-60)) and self.manualControlFlag==False and startupTime.total_seconds() >= self.timeToResume):
            log.add_log("AUTO main light -> ON")
            self.lamp_on(self.pin)
            self.flag=1
            time.sleep(20)
        if(self.flag==1 and (int(offTimeDifference.total_seconds())>0) and (int(offTimeDifference.total_seconds())<60) and self.manualControlFlag==False):
            log.add_log("AUTO main light -> OFF")
            """lampaHalogen.czasPWMustawienie=0
            lampaHalogen.pwmWymagane=100
            for i in range(30):
                if(lampaHalogen.pwm==100):
                    break;
                time.sleep(1)
            lampaHalogen.czasPWMustawienie=1"""
            self.lamp_off(self.pin)
            """lampaHalogen.czasPWMustawienie=(self.czasWygaszania*60)/100
            lampaHalogen.pwmWymagane=0"""
            self.flag=0
            time.sleep(20)

    def lamp_on(self, pin):
        GPIO.output(pin, GPIO.HIGH)

    def lamp_off(self, pin):
        GPIO.output(pin, GPIO.LOW)

mainLight = MAIN_LIGHT_CL(19, '8:00:00.0000', '19:15:00.0000')
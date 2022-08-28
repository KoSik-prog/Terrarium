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
import RPi.GPIO as GPIO
from timeit import default_timer as timer

from libraries.log import *

class MAIN_LIGHT_CL:
    flag = False
    """AutoON = '8:00:00.0000'
    AutoOFF = '19:15:00.0000'#'19:45:00.0000'"""
    dimmingTime = 12 #czas stopniowego wygaszania w minutach
    manualControlFlag = False
    timeToResume = 30 #seconds - czas do wlaczenia lampy po ponownym uruchomieniu

    def __init__(self, AutoON, AutoOFF):
        self.AutoON = AutoON
        self.AutoOFF = AutoOFF

    def lamp_on(self, pin):
        GPIO.output(pin, GPIO.HIGH)

    def lamp_off(self, pin):
        GPIO.output(pin, GPIO.LOW)

    def check_timer(self, deviceStartTime):
        format = '%H:%M:%S.%f'
        aktual=datetime.datetime.now().time()

        try:
            zmiennaON = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(self.AutoON, format) # obliczenie roznicy czasu
        except ValueError as e:
            log.add_log('Blad czasu wł:', e)
        try:
            zmiennaOFF = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(self.AutoOFF, format) # obliczenie roznicy czasu
        except ValueError as e:
            log.add_log('Blad czasu wył:', e)
        #-----skasowanie flag ----------
        if(int(zmiennaON.total_seconds())>(-15) and int(zmiennaON.total_seconds())<0 and  self.manualControlFlag==True):
            self.manualControlFlag=False
        if(int(zmiennaOFF.total_seconds())>(-15) and int(zmiennaOFF.total_seconds())<0 and self.manualControlFlag==True):
            self.manualControlFlag=False
        #------SPRAWDZENIE------------------------
        end = timer()
        czasOdUruchomienia = datetime.timedelta(seconds=round(end - deviceStartTime))
        if(self.flag==0 and (int(zmiennaON.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<(-60)) and self.manualControlFlag==False and czasOdUruchomienia.total_seconds() >= self.timeToResume):
            log.add_log("AUTO MHG -> ON")
            GPIO.output(19, GPIO.HIGH) #Metalohalogen
            self.flag=1
            time.sleep(20)
        if(self.flag==1 and (int(zmiennaOFF.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<60) and self.manualControlFlag==False):
            log.add_log("AUTO MHG -> OFF")
            """lampaHalogen.czasPWMustawienie=0
            lampaHalogen.pwmWymagane=100
            for i in range(30):
                if(lampaHalogen.pwm==100):
                    break;
                time.sleep(1)
            lampaHalogen.czasPWMustawienie=1"""
            self.lamp_off()
            """lampaHalogen.czasPWMustawienie=(self.czasWygaszania*60)/100
            lampaHalogen.pwmWymagane=0"""
            self.flag=0
            time.sleep(20)
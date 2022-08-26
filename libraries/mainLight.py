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

from log import *

class MAIN_LIGHT:
    flag = False
    AutoON = '8:00:00.0000'
    AutoOFF = '19:15:00.0000'#'19:45:00.0000'
    dimmingTime = 12 #czas stopniowego wygaszania w minutach
    manualControlFlag = False

    def __init__(self, address):

    def lamp_on(self, pin):
        GPIO.output(pin, GPIO.HIGH)

    def lamp_off(self, pin):
        GPIO.output(pin, GPIO.LOW)

    def timerMetalohalogen(self, deviceStartTime):

        format = '%H:%M:%S.%f'
        aktual=datetime.datetime.now().time()

        try:
            zmiennaON = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(self.AutoON, format) # obliczenie roznicy czasu
        except ValueError as e:
            log('Blad czasu wł:', e)
        try:
            zmiennaOFF = datetime.datetime.strptime(str(aktual), format) - datetime.datetime.strptime(self.AutoOFF, format) # obliczenie roznicy czasu
        except ValueError as e:
            print('Blad czasu wył:', e)
        #-----skasowanie flag ----------
        if(int(zmiennaON.total_seconds())>(-15) and int(zmiennaON.total_seconds())<0 and  lampaMHG.manualControlFlag==True):
            lampaMHG.manualControlFlag=False
        if(int(zmiennaOFF.total_seconds())>(-15) and int(zmiennaOFF.total_seconds())<0 and lampaMHG.manualControlFlag==True):
            lampaMHG.manualControlFlag=False
        #------SPRAWDZENIE------------------------
        end = timer()
        czasOdUruchomienia = datetime.timedelta(seconds=round(end-deviceStartTime))
        if(lampaMHG.Flaga==0 and (int(zmiennaON.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<(-60)) and lampaMHG.manualControlFlag==False and czasOdUruchomienia.total_seconds() >= 300):
            zapis_dziennika_zdarzen("AUTO MHG -> ON")
            GPIO.output(19, GPIO.HIGH) #Metalohalogen
            lampaMHG.Flaga=1
            time.sleep(20)
        if(lampaMHG.Flaga==1 and (int(zmiennaOFF.total_seconds())>0) and (int(zmiennaOFF.total_seconds())<60) and lampaMHG.manualControlFlag==False):
            zapis_dziennika_zdarzen("AUTO MHG -> OFF")
            lampaHalogen.czasPWMustawienie=0
            lampaHalogen.pwmWymagane=100
            for i in range(30):
                if(lampaHalogen.pwm==100):
                    break;
                time.sleep(1)
            lampaHalogen.czasPWMustawienie=1
            GPIO.output(19, GPIO.LOW) #Metalohalogen
            lampaHalogen.czasPWMustawienie=(lampaMHG.czasWygaszania*60)/100
            lampaHalogen.pwmWymagane=0
            lampaMHG.Flaga=0
            time.sleep(20)